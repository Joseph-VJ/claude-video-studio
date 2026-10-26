"""Design audit for a rendered video or PNG frame folder.

Writes a contact sheet, a palette strip and design-audit.json with neon /
oversaturation share, distinct accent hues, pure black/white share and a
banding-risk estimate. The numbers support a visual review; they do not
judge taste. Footage pixels (skin, wardrobe) are counted too, so read the
sheet alongside the numbers.
"""
import argparse, json, pathlib, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

NEON_S, NEON_V = 0.80, 0.85          # drawn graphics should stay below this pair
OVERSAT_S, OVERSAT_V = 0.65, 0.50
ACCENT_S, ACCENT_V = 0.45, 0.35      # "clearly coloured" pixel
HUE_BINS = 24                        # 15 degrees each
HUE_MIN_SHARE = 0.004                # a hue bin counts when >= 0.4% of a frame
SMOOTH_BLOCK, SMOOTH_STD = 16, 0.8   # 16x16 luma blocks with std < 0.8 levels
ANALYSIS_W = 1080   # native width: grain/dither is invisible to the banding check if the frame is downscaled first

def hsv(rgb):
    x = rgb.astype(np.float32) / 255.0
    mx, mn = x.max(-1), x.min(-1)
    c = mx - mn
    s = np.where(mx > 0, c / np.maximum(mx, 1e-6), 0)
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    safe = np.maximum(c, 1e-6)
    h = np.where(mx == r, ((g - b) / safe) % 6, np.where(mx == g, (b - r) / safe + 2, (r - g) / safe + 4)) * 60
    h = np.where(c > 0, h, 0)
    return h, s, mx

def frame_metrics(rgb):
    h, s, v = hsv(rgb)
    n = s.size
    accent = (s >= ACCENT_S) & (v >= ACCENT_V)
    hist = np.bincount((h[accent] / (360 / HUE_BINS)).astype(int) % HUE_BINS, minlength=HUE_BINS) / n
    luma = rgb.astype(np.float32) @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    bh, bw = luma.shape[0] // SMOOTH_BLOCK, luma.shape[1] // SMOOTH_BLOCK
    blocks = luma[:bh * SMOOTH_BLOCK, :bw * SMOOTH_BLOCK].reshape(bh, SMOOTH_BLOCK, bw, SMOOTH_BLOCK)
    std, mean = blocks.std((1, 3)), blocks.mean((1, 3))
    smooth = (std < SMOOTH_STD) & (mean > 12) & (mean < 243)
    return {
        "neon_share": round(float(((s >= NEON_S) & (v >= NEON_V)).sum() / n), 5),
        "oversat_share": round(float(((s >= OVERSAT_S) & (v >= OVERSAT_V)).sum() / n), 5),
        "accent_hue_bins": [int(i * 360 / HUE_BINS) for i in np.nonzero(hist >= HUE_MIN_SHARE)[0]],
        "pure_black_share": round(float((rgb.max(-1) <= 8).sum() / n), 4),
        "pure_white_share": round(float((rgb.min(-1) >= 247).sum() / n), 4),
        "smooth_block_share": round(float(smooth.mean()), 4),
    }, hist

def video_frames(path, every, width=None):
    import av
    with av.open(str(path)) as c:
        stream = c.streams.video[0]
        next_t = 0.0
        for f in c.decode(stream):
            t = float(f.time or 0)
            if t + 1e-6 < next_t: continue
            next_t = t + every
            w = width or ANALYSIS_W
            h = int(round(f.height * w / f.width / 2)) * 2
            yield t, f.reformat(width=w, height=h, format="rgb24").to_ndarray()

def folder_frames(path, every, fps, width=None):
    files = sorted(path.glob("*.png"))
    step = max(1, int(round(every * fps)))
    for i in range(0, len(files), step):
        im = Image.open(files[i]).convert("RGB")
        w = width or ANALYSIS_W
        if im.width != w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        yield i / fps, np.asarray(im)

def contact_sheet(thumbs, cols, out):
    tw, th = thumbs[0][1].size
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=14)
    for i, (t, im) in enumerate(thumbs):
        x, y = (i % cols) * tw, (i // cols) * (th + 22)
        sheet.paste(im, (x, y + 22))
        d.text((x + 4, y + 3), f"{t:6.2f}s", fill=(230, 230, 230), font=font)
    sheet.save(out)

def palette(samples, k, out):
    mosaic = Image.fromarray(np.concatenate(samples, axis=0))
    q = mosaic.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = np.array(q.getpalette()[:k * 3]).reshape(-1, 3)
    counts = np.bincount(np.asarray(q).ravel(), minlength=k)[:k]
    order = np.argsort(-counts)
    entries = [{"hex": "#%02X%02X%02X" % tuple(pal[i]), "share": round(float(counts[i] / counts.sum()), 4)} for i in order]
    strip = Image.new("RGB", (k * 120, 150), (255, 255, 255))
    d = ImageDraw.Draw(strip)
    font = ImageFont.load_default(size=16)
    for j, e in enumerate(entries):
        d.rectangle([j * 120, 0, j * 120 + 119, 110], fill=e["hex"])
        d.text((j * 120 + 6, 116), f"{e['hex']}\n{e['share'] * 100:.1f}%", fill=(20, 20, 20), font=font)
    strip.save(out)
    return entries

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="video file or folder of PNG frames")
    ap.add_argument("--out", required=True, help="output folder (inside the project, e.g. PROJECT/qa/design-audit)")
    ap.add_argument("--every", type=float, default=1.0, help="seconds between sampled frames")
    ap.add_argument("--fps", type=float, default=30.0, help="frame rate of a PNG folder")
    ap.add_argument("--cols", type=int, default=10)
    ap.add_argument("--palette", type=int, default=12)
    ap.add_argument("--width", type=int, default=ANALYSIS_W, help="analysis width in px (default native 1080; smaller is faster but averages grain away)")
    ap.add_argument("--baseline", help="graded a-roll or source video without graphics; its own colour levels raise the thresholds so footage (e.g. a red shirt) is not blamed on the graphics")
    a = ap.parse_args()
    src, out = pathlib.Path(a.source), pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    neon_thr, hue_thr, baseline = 0.01, 4, None
    if a.baseline:
        base = [frame_metrics(rgb)[0] for _, rgb in video_frames(pathlib.Path(a.baseline), max(a.every, 2.0), a.width)]
        b_neon = float(np.percentile([r["neon_share"] for r in base], 90))
        b_hues = int(np.percentile([len(r["accent_hue_bins"]) for r in base], 90))
        neon_thr, hue_thr = b_neon + 0.01, max(4, b_hues + 1)
        baseline = {"source": str(pathlib.Path(a.baseline).resolve()), "frames": len(base), "neon_p90": round(b_neon, 5), "accent_hue_bins_p90": b_hues}
    frames = folder_frames(src, a.every, a.fps, a.width) if src.is_dir() else video_frames(src, a.every, a.width)
    per, thumbs, samples, hist_sum = [], [], [], np.zeros(HUE_BINS)
    for t, rgb in frames:
        m, hist = frame_metrics(rgb)
        hist_sum += hist
        per.append({"t": round(t, 3), **m})
        im = Image.fromarray(rgb)
        thumbs.append((t, im.resize((216, int(im.height * 216 / im.width)), Image.LANCZOS)))
        samples.append(np.asarray(im.resize((90, int(im.height * 90 / im.width)), Image.BILINEAR)))
    if not per: raise SystemExit("no frames read from " + str(src))
    contact_sheet(thumbs, a.cols, out / "contact-sheet.png")
    entries = palette(samples, a.palette, out / "palette.png")
    mean_hist = hist_sum / len(per)
    video_hues = [int(i * 360 / HUE_BINS) for i in np.nonzero(mean_hist >= HUE_MIN_SHARE / 2)[0]]
    worst_neon = max(per, key=lambda r: r["neon_share"])
    flags = []
    floods = [r for r in per if r["neon_share"] > 0.25]
    if floods:
        flags.append(f"full-screen neon flood in {len(floods)} sampled frames, e.g. {floods[0]['t']}s ({floods[0]['neon_share'] * 100:.0f}% of the frame)")
    neon = [r for r in per if r["neon_share"] > neon_thr]
    if len(neon) > 0.10 * len(per):
        flags.append(f"{len(neon)}/{len(per)} sampled frames have more than {neon_thr * 100:.1f}% neon pixels, e.g. {neon[0]['t']}s (check whether graphics or footage)")
    many = [r for r in per if len(r["accent_hue_bins"]) > hue_thr]
    if len(many) > 0.15 * len(per):
        flags.append(f"{len(many)}/{len(per)} sampled frames show more than {hue_thr} distinct accent hue bins (rainbow risk), e.g. {many[0]['t']}s")
    if len(video_hues) > 6:
        flags.append(f"{len(video_hues)} accent hue bins across the video: palette may not be one system")
    hot = [r for r in per if r["smooth_block_share"] > 0.35]
    if hot:
        flags.append(f"{len(hot)} frames are >35% smooth flat area (check gradients/dark fields for banding; add grain), e.g. {hot[0]['t']}s")
    report = {
        "source": str(src.resolve()),
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "sampled_frames": len(per),
        "every_s": a.every,
        "baseline": baseline,
        "thresholds": {"neon_frame_share": neon_thr, "accent_hue_bins_per_frame": hue_thr, "neon": [NEON_S, NEON_V], "oversat": [OVERSAT_S, OVERSAT_V], "accent": [ACCENT_S, ACCENT_V], "hue_bin_deg": 360 / HUE_BINS, "hue_min_share": HUE_MIN_SHARE, "smooth_block": [SMOOTH_BLOCK, SMOOTH_STD]},
        "summary": {
            "max_neon_share": worst_neon["neon_share"],
            "max_neon_at_s": worst_neon["t"],
            "mean_oversat_share": round(float(np.mean([r["oversat_share"] for r in per])), 5),
            "video_accent_hue_bins_deg": video_hues,
            "max_accent_hue_bins_in_one_frame": max(len(r["accent_hue_bins"]) for r in per),
            "share_frames_over_hue_threshold": round(len(many) / len(per), 3),
            "share_frames_over_neon_threshold": round(len(neon) / len(per), 3),
            "mean_pure_black_share": round(float(np.mean([r["pure_black_share"] for r in per])), 4),
            "mean_pure_white_share": round(float(np.mean([r["pure_white_share"] for r in per])), 4),
            "max_smooth_block_share": max(r["smooth_block_share"] for r in per),
        },
        "palette": entries,
        "flags": flags,
        "note": "Footage pixels are included: skin and wardrobe add hue bins. Judge flags against the contact sheet; numbers are not a taste score.",
        "frames": per,
    }
    (out / "design-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"out": str(out.resolve()), "summary": report["summary"], "flags": flags}, indent=2))

if __name__ == "__main__":
    main()
