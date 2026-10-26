"""Cut-first graded timeline renderer for the CURRENT job (any new video).

Decodes ONLY the edit's source segments, runs RVM matting in CPU worker processes (recurrent state reset at every cut,
with a short warm-up), grades every frame in ONE colour process (CuPy GPU or NumPy CPU), and encodes the edited a-roll
directly. Compared with render-colour-fast.py + join + per-cut recut it removes: the full-length grade of unused frames,
the 16-bit chunk files, the physical join, and the 28 cut encodes + second join encode.

Outputs (all explicit in the config, all fresh paths inside E:/Video):
  aroll    H.264 for the graphics timeline: x264 CRF, NVENC const-QP, or NVENC/x264 mathematically lossless.
  archive  optional FFV1 16-bit RGB of the graded edited frames (decoded-frame lossless, large).
Audio (optional) is cut with the same segment list (6 ms edge fades) and muxed without touching the picture.

The colour module must expose the same interface as render-colour-fast.py: R, MASK, luma, smoothstep, box_blur and
correct(base, face, parameters, shirt_gains, alpha=...). Its parameters must be the current video's reviewed values:
every key in R must be given explicitly. Old project or lab settings are never inherited.
Usage: python render-timeline-colour.py CONFIG.json
"""
import os, sys, json, time, types, uuid, hashlib, pathlib, subprocess, importlib.util
import numpy as np

ROOT = pathlib.Path("E:/Video")
sys.path.insert(0, str(ROOT / "scripts"))
SLOTS = 4                                    # shared-memory frame slots per worker (bounded RAM, no big pickles)


def hash_file(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_into(stream, view):
    pos, n = 0, len(view)
    while pos < n:
        c = stream.readinto(view[pos:])
        if not c:
            raise RuntimeError("Truncated or missing decoded frame")
        pos += c


def decode_filter(pre, eb, ef):
    if pre != "hlg-hable-bt709":
        raise ValueError("Only the reviewed HLG BT.2020 -> Hable -> Rec.709 preprocessing is supported; add and review another path first")
    return ("[0:v]fps=30,zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,split[l1][l2];"
            f"[l1]exposure=exposure={eb},tonemap=tonemap=hable:desat=0,zscale=t=bt709,format=gbrp16le[b];"
            f"[l2]exposure=exposure={ef},tonemap=tonemap=hable:desat=0,zscale=t=bt709,format=gbrp16le[f];[b][f]hstack,format=gbrp16le")


# ---------------------------------------------------------------- worker: decode + matte, one segment at a time
def worker(wid, jobs, cfg, shm_name, free_q, out_q):
    print(f"worker {wid} started (pid {os.getpid()})", file=sys.stderr, flush=True)
    from multiprocessing import shared_memory
    W, H, fps = cfg["width"], cfg["height"], cfg["fps"]
    p = cfg["parameters"]
    fb = 2 * W * H * 3 * 2                    # base|face side by side, 16-bit planar G,B,R
    ab = W * H * 4                            # float32 alpha
    shm = shared_memory.SharedMemory(name=shm_name)
    session = None
    if cfg["matte"]:
        from studio_gpu import matting_session
        session = matting_session(gpu=False, threads=int(cfg["matte_threads"]))
    fc = decode_filter(cfg["preprocess"], p["exposure_ev"], p["exposure_ev"] + p["face_ev"])
    t_dec = t_mat = 0.0
    scratch = bytearray(fb)
    try:
        for si, s in jobs:
            n = int(s["frames"])
            warm = min(int(cfg["matte_warmup_frames"]), int(round(s["in"] * fps))) if session else 0
            start = s["in"] - warm / fps
            cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{start:.6f}", "-threads", str(cfg["decode_threads"]), "-i", cfg["input"],
                   "-filter_complex", fc, "-frames:v", str(n + warm), "-f", "rawvideo", "-pix_fmt", "gbrp16le", "pipe:1"]
            d = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
            rec = [np.zeros((1, 1, 1, 1), np.float32) for _ in range(4)]
            for k in range(n + warm):
                if k < warm:
                    t = time.perf_counter(); read_into(d.stdout, memoryview(scratch)); t_dec += time.perf_counter() - t
                    z = np.frombuffer(scratch, "<u2").reshape(3, H, 2 * W)
                    base = np.stack([z[2, :, :W], z[0, :, :W], z[1, :, :W]]).astype(np.float32) / 65535
                    t = time.perf_counter()
                    feeds = {"src": base[None], "downsample_ratio": np.array([min(512 / max(W, H), 1)], np.float32)}
                    feeds.update({f"r{i+1}i": r for i, r in enumerate(rec)})
                    _, _, *rec = session.run(None, feeds); t_mat += time.perf_counter() - t
                    continue
                slot = free_q.get()                                   # wait for a free slot (backpressure)
                off = slot * (fb + ab)
                view = memoryview(shm.buf)[off:off + fb]
                t = time.perf_counter(); read_into(d.stdout, view); t_dec += time.perf_counter() - t
                if session:
                    z = np.frombuffer(shm.buf, "<u2", count=3 * H * 2 * W, offset=off).reshape(3, H, 2 * W)
                    base = np.stack([z[2, :, :W], z[0, :, :W], z[1, :, :W]]).astype(np.float32) / 65535
                    t = time.perf_counter()
                    feeds = {"src": base[None], "downsample_ratio": np.array([min(512 / max(W, H), 1)], np.float32)}
                    feeds.update({f"r{i+1}i": r for i, r in enumerate(rec)})
                    _, pha, *rec = session.run(None, feeds)
                    np.frombuffer(shm.buf, np.float32, count=W * H, offset=off + fb)[:] = pha[0, 0].reshape(-1)
                    t_mat += time.perf_counter() - t
                del view
                out_q.put((si, k - warm, slot))
            d.stdout.close(); err = d.stderr.read().decode(errors="replace"); rc = d.wait()
            if rc:
                raise RuntimeError(f"decode failed for segment {si}: {err[-400:]}")
        out_q.put(("done", wid, {"decode": t_dec, "matte": t_mat}))
    except Exception as e:                                            # surface worker errors to the main process
        out_q.put(("error", wid, repr(e)))
    finally:
        z = base = view = None                                        # drop views into shared memory before closing it
        try:
            shm.close()
        except BufferError:
            pass


# ---------------------------------------------------------------- colour module loading (same swap as render-colour-fast.py)
def load_module(cfg):
    path = pathlib.Path(cfg["grade_module"]).resolve()
    if cfg.get("module_sha256") and cfg["module_sha256"] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError("Colour module changed; review parameters before rendering")
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("job_colour", path); gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
    missing = set(getattr(gm, "R", {})) - set(cfg["parameters"])
    if missing:
        raise ValueError("Explicit parameters required; refusing inherited defaults: " + str(sorted(missing)))
    cp = None
    if cfg["compute"] == "gpu":
        from studio_gpu import load_cupy
        cp = load_cupy(); gm.np = cp; gm.MASK = cp.asarray(gm.MASK)
        for name in ["luma", "smoothstep", "box_blur"]:
            fn = getattr(gm, name); setattr(gm, name, types.FunctionType(fn.__code__, {**fn.__globals__, "np": cp}, fn.__name__, fn.__defaults__, fn.__closure__))
        if cfg["fast_blur_float32"]:
            def box_blur32(a, r):                                     # same separable 3-pass box blur, float32 accumulation (GTX 16xx float64 is ~1/32 speed)
                for axis in (0, 1):
                    for _ in range(3):
                        pad = [(0, 0), (0, 0)]; pad[axis] = (r + 1, r)
                        c = cp.cumsum(cp.pad(a, pad, mode="reflect"), axis=axis, dtype=cp.float32)
                        n = a.shape[axis]
                        a = ((cp.take(c, cp.arange(2 * r + 1, 2 * r + 1 + n), axis=axis) - cp.take(c, cp.arange(0, n), axis=axis)) / (2 * r + 1)).astype(cp.float32)
                return a
            gm.box_blur = box_blur32
    elif cfg["compute"] != "cpu":
        raise ValueError("compute must be cpu or gpu")
    return gm, cp, path


def aroll_encoder(cfg, path):
    a = cfg["aroll"]; W, H = cfg["width"], cfg["height"]
    conv = "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", str(cfg["fps"]), "-i", "pipe:0", "-an"]
    enc = a["encoder"]
    if enc == "x264":
        cmd += ["-vf", conv, "-c:v", "libx264", "-preset", a.get("preset", "fast"), "-crf", str(a["quality"]), "-threads", str(a.get("threads", 2))]
    elif enc == "nvenc":
        cmd += ["-vf", conv, "-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq", "-rc", "constqp", "-qp", str(a["quality"])]
    elif enc == "nvenc-lossless":
        cmd += ["-vf", conv, "-c:v", "h264_nvenc", "-preset", "p5", "-tune", "lossless"]
    else:
        raise ValueError("aroll encoder must be x264, nvenc or nvenc-lossless")
    cmd += ["-g", str(a.get("gop", 30)), "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_trc", "bt709", "-color_primaries", "bt709", str(path)]
    return cmd


def audio_cut(cfg, out_wav):
    au = cfg["audio"]; fps = cfg["fps"]; segs = cfg["segments"]; fade = au.get("fade_ms", 6) / 1000
    parts = []; labels = []
    for i, s in enumerate(segs):
        dur = s["frames"] / fps
        parts.append(f"[0:a]atrim=start={s['in']:.6f}:duration={dur:.6f},asetpts=PTS-STARTPTS,apad,atrim=duration={dur:.6f},"
                     f"afade=t=in:d={fade},afade=t=out:st={max(0, dur - fade):.6f}:d={fade}[a{i}]")
        labels.append(f"[a{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=0:a=1[a]"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", au["source"], "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)], check=True)


def main():
    import multiprocessing as mp
    from multiprocessing import shared_memory
    cfgpath = pathlib.Path(sys.argv[1]).resolve(); cfg = json.loads(cfgpath.read_text(encoding="utf-8-sig"))
    for key in ["input", "segments", "grade_module", "parameters", "shirt_gains", "width", "height", "fps", "preprocess", "compute",
                "fast_blur_float32", "matte", "matte_warmup_frames", "matte_threads", "decode_threads", "cpu_workers", "dither_strength", "dither_seed", "aroll"]:
        if key not in cfg:
            raise ValueError(f"Explicit config key required: {key}")
    W, H, fps = cfg["width"], cfg["height"], cfg["fps"]
    if (W, H, fps) != (1080, 1920, 30):
        raise ValueError("This renderer is reviewed for 1080x1920 at 30 fps (the colour module's mask geometry)")
    src = pathlib.Path(cfg["input"]).resolve()
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_streams", "-of", "json", str(src)]))["streams"][0]
    if info.get("color_transfer") != "arib-std-b67" or info.get("color_primaries") != "bt2020":
        raise ValueError("Source is not HLG BT.2020; this reviewed path would misinterpret it")
    outs = [pathlib.Path(cfg["aroll"]["path"]).resolve()] + ([pathlib.Path(cfg["archive"]["path"]).resolve()] if cfg.get("archive") else [])
    for o in outs:
        if not o.is_relative_to(ROOT.resolve()) or o.exists():
            raise ValueError(f"Use a fresh output inside E:/Video: {o}")
        o.parent.mkdir(parents=True, exist_ok=True)
    strength = float(cfg["dither_strength"])
    if not 0 <= strength <= 1 / 255:
        raise ValueError("Dither strength must be within 0..1/255")
    segs = cfg["segments"]; total = sum(int(s["frames"]) for s in segs)
    gm, cp, modpath = load_module(cfg)
    params = cfg["parameters"]; gains = cfg["shirt_gains"]
    rng = np.random.default_rng(int(cfg["dither_seed"]))
    noise_k = None
    if cp is not None:
        # deterministic per-pixel dither noise on the GPU (PCG hash of pixel index and frame), uniform in [-0.5, 0.5)
        noise_k = cp.ElementwiseKernel("uint32 seed", "float32 out",
            "unsigned int x = (unsigned int)i * 747796405u + seed * 2891336453u + 1u;"
            "x = ((x >> ((x >> 28u) + 4u)) ^ x) * 277803737u; x = (x >> 22u) ^ x;"
            "out = (float)x * (1.0f / 4294967296.0f) - 0.5f;", "pcg_dither")
    if cp is not None:
        # compile every GPU kernel now, before the CPU workers load the machine (CuPy's library probe has a 10 s timeout)
        t = time.perf_counter()
        zb = cp.zeros((3, H, W), cp.float32) + 0.5; za = cp.zeros((H, W), cp.float32)
        r0 = gm.correct(zb, zb, params, gains, alpha=za if cfg["matte"] else None)
        nz = cp.empty(r0.shape, cp.float32); noise_k(cp.uint32(1), nz)
        cp.asnumpy((cp.clip(r0 + nz, 0, 1).transpose(1, 2, 0) * 65535 + 0.5).astype(cp.uint16)); cp.cuda.Stream.null.synchronize()
        print(f"GPU kernels compiled/warmed in {time.perf_counter() - t:.1f} s", flush=True)
        del zb, za, r0, nz
    t_all = time.perf_counter()

    K = int(cfg["cpu_workers"]); fb = 2 * W * H * 3 * 2; ab = W * H * 4
    shms = [shared_memory.SharedMemory(create=True, size=SLOTS * (fb + ab)) for _ in range(K)]
    ctx = mp.get_context("spawn")
    free_qs = [ctx.Queue() for _ in range(K)]; out_qs = [ctx.Queue() for _ in range(K)]
    for q in free_qs:
        for s in range(SLOTS):
            q.put(s)
    jobs = [[] for _ in range(K)]
    for si, s in enumerate(segs):
        jobs[si % K].append((si, s))
    procs = [ctx.Process(target=worker, args=(w, jobs[w], cfg, shms[w].name, free_qs[w], out_qs[w]), daemon=True) for w in range(K)]
    for pr in procs:
        pr.start()
    print(f"started {K} CPU workers", flush=True)

    tmp_video = outs[0].with_name(outs[0].stem + ".video-" + uuid.uuid4().hex[:8] + ".mp4")
    enc = subprocess.Popen(aroll_encoder(cfg, tmp_video), stdin=subprocess.PIPE)
    arc = None; tmp_arc = None
    if cfg.get("archive"):
        tmp_arc = outs[1].with_name(outs[1].stem + ".partial-" + uuid.uuid4().hex[:8] + ".mkv")
        arc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", str(fps), "-i", "pipe:0",
                                "-c:v", "ffv1", "-level", "3", "-slicecrc", "1", "-pix_fmt", "gbrp16le", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "rgb", "-color_range", "pc", str(tmp_arc)], stdin=subprocess.PIPE)
    import threading, queue as _queue
    wq = _queue.Queue(maxsize=6); werr = []
    def writer():
        try:
            while True:
                item = wq.get()
                if item is None:
                    return
                enc.stdin.write(item)
                if arc:
                    arc.stdin.write(item)
        except Exception as e:
            werr.append(repr(e))
    wt = threading.Thread(target=writer, daemon=True); wt.start()
    timing = {"wait_for_workers": 0.0, "colour": 0.0, "write": 0.0}; worker_timing = {}
    done = 0; t_first = None; z = alpha = buf = None
    try:
        for si, s in enumerate(segs):
            w = si % K
            for k in range(int(s["frames"])):
                t = time.perf_counter()
                msg = out_qs[w].get()
                if msg[0] == "error":
                    raise RuntimeError(f"worker {msg[1]} failed: {msg[2]}")
                if msg[0] == "done":
                    raise RuntimeError(f"worker {w} finished early before segment {si} frame {k}")
                msi, mk, slot = msg
                if (msi, mk) != (si, k):
                    raise RuntimeError(f"frame order mismatch: got {(msi, mk)} expected {(si, k)}")
                timing["wait_for_workers"] += time.perf_counter() - t
                t = time.perf_counter()
                off = slot * (fb + ab); buf = shms[w].buf
                z = np.frombuffer(buf, "<u2", count=3 * H * 2 * W, offset=off).reshape(3, H, 2 * W)
                alpha = np.frombuffer(buf, np.float32, count=W * H, offset=off + fb).reshape(H, W) if cfg["matte"] else None
                if cp is not None:
                    zg = cp.asarray(z); ag = None if alpha is None else cp.asarray(alpha)
                    free_qs[w].put(slot)                                  # slot can be refilled while the GPU works
                    zg = zg.astype(cp.float32) / 65535
                    base = cp.stack([zg[2, :, :W], zg[0, :, :W], zg[1, :, :W]]); face = cp.stack([zg[2, :, W:], zg[0, :, W:], zg[1, :, W:]])
                    res = gm.correct(base, face, params, gains, alpha=ag)
                    if strength:
                        nz = cp.empty(res.shape, cp.float32); noise_k(cp.uint32(int(cfg["dither_seed"]) * 100003 + done), nz)
                        res = res + nz * strength
                    pix = cp.asnumpy((cp.clip(res, 0, 1).transpose(1, 2, 0) * 65535 + 0.5).astype(cp.uint16)).tobytes()
                    out = None
                else:
                    zf = z.astype(np.float32) / 65535; a2 = None if alpha is None else alpha.copy()
                    free_qs[w].put(slot)
                    base = np.stack([zf[2, :, :W], zf[0, :, :W], zf[1, :, :W]]); face = np.stack([zf[2, :, W:], zf[0, :, W:], zf[1, :, W:]])
                    out = gm.correct(base, face, params, gains, alpha=a2)
                    if strength:
                        out = out + (rng.random(out.shape, dtype=np.float32) - 0.5) * strength
                    pix = (np.clip(out, 0, 1).transpose(1, 2, 0) * 65535 + 0.5).astype("<u2").tobytes()
                timing["colour"] += time.perf_counter() - t
                t = time.perf_counter()
                if werr:
                    raise RuntimeError("encoder writer failed: " + werr[0])
                wq.put(pix)                                               # blocks only if the encoder falls behind
                timing["write"] += time.perf_counter() - t
                done += 1
                if t_first is None:
                    t_first = time.perf_counter() - t_all
                if done % 60 == 0:
                    el = time.perf_counter() - t_all
                    print(f"{done}/{total} frames  {done / el:.2f} fps  eta {(total - done) / max(done / el, 1e-6) / 60:.1f} min", flush=True)
        for w in range(K):
            msg = out_qs[w].get(timeout=120)
            if msg[0] == "error":
                raise RuntimeError(f"worker {msg[1]} failed: {msg[2]}")
            worker_timing[f"worker{w}"] = msg[2]
        wq.put(None); wt.join()
        if werr:
            raise RuntimeError("encoder writer failed: " + werr[0])
        enc.stdin.close(); rc = enc.wait()
        rca = 0
        if arc:
            arc.stdin.close(); rca = arc.wait()
        if rc or rca:
            raise RuntimeError(f"encoder exit codes aroll={rc} archive={rca}")
        t_enc_done = time.perf_counter() - t_all
        # audio: cut with the same segments, mux without touching the picture
        if cfg.get("audio"):
            wav = outs[0].with_name(outs[0].stem + ".audio-" + uuid.uuid4().hex[:8] + ".wav")
            audio_cut(cfg, wav)
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(tmp_video), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                            "-c:a", cfg["audio"].get("codec", "aac"), "-b:a", cfg["audio"].get("bitrate", "192k"), "-shortest", "-movflags", "+faststart", str(outs[0])], check=True)
            tmp_video.unlink(); wav.unlink()
        else:
            tmp_video.rename(outs[0])
        if tmp_arc:
            tmp_arc.rename(outs[1])
        frames_out = int(json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "json", str(outs[0])]))["streams"][0]["nb_read_frames"])
        if frames_out != total:
            raise RuntimeError(f"a-roll has {frames_out} frames, expected {total}")
        rec = {"scope": "cut-first decode + CPU matting + selected colour compute + direct a-roll encode (+ optional FFV1 archive) + audio cut/mux",
               "frames": total, "segments": len(segs), "seconds_total": time.perf_counter() - t_all, "seconds_to_video_encoded": t_enc_done,
               "seconds_to_first_frame": t_first, "fps": total / (time.perf_counter() - t_all), "main_timing": timing, "worker_timing": worker_timing,
               "compute": cfg["compute"], "fast_blur_float32": cfg["fast_blur_float32"], "cpu_workers": K,
               "outputs": [str(o) for o in outs], "config": {k: v for k, v in cfg.items() if k != "parameters"}, "parameters": params,
               "module_sha256": hash_file(modpath), "source_sha256": hash_file(src), "renderer_sha256": hash_file(__file__)}
        pathlib.Path(str(outs[0]) + ".render.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
        print(json.dumps({k: rec[k] for k in ["frames", "seconds_total", "fps", "main_timing", "worker_timing"]}, indent=1), flush=True)
    finally:
        for pr in procs:
            if pr.is_alive():
                pr.terminate()
        for p_ in [enc, arc]:
            if p_ and p_.poll() is None:
                p_.kill()
        z = alpha = buf = None                                          # drop numpy views into shared memory before closing it
        for shm in shms:
            try:
                shm.close()
            except BufferError:
                pass
            shm.unlink()
        for f in [tmp_video, tmp_arc]:
            if f and pathlib.Path(f).exists():
                pathlib.Path(f).unlink()


if __name__ == "__main__":
    main()
