"""Stream a current-job colour function through CPU or verified GPU compute.
Configuration must explicitly name sources, parameters and output; no previous look is selected.
"""
import os,sys,pathlib,json,subprocess,time,hashlib,types,uuid
import numpy as np
ROOT=pathlib.Path("E:/Video");sys.path.insert(0,str(ROOT/"scripts"))
from studio_gpu import load_cupy,matting_session
def hash_file(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for block in iter(lambda:f.read(8*1024*1024),b""):h.update(block)
    return h.hexdigest()

def read_exact(stream,n):
    # FileIO.read(remaining) repeatedly allocates a huge bytes object on Windows'
    # small anonymous pipe reads. Reuse one frame buffer and read into its view.
    buffer=bytearray(n);view=memoryview(buffer);position=0
    while position<n:
        count=stream.readinto(view[position:])
        if not count:raise RuntimeError("Truncated or missing decoded frame")
        position+=count
    return buffer

def main():
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("config");a=ap.parse_args()
    cfgpath=pathlib.Path(a.config).resolve();c=json.loads(cfgpath.read_text(encoding="utf-8-sig"))
    src=pathlib.Path(c["input"]).resolve();out=pathlib.Path(c["output"]).resolve();modulepath=pathlib.Path(c["grade_module"]).resolve()
    if not src.is_file() or not modulepath.is_file():raise FileNotFoundError("Missing current-job source or colour module")
    module_hash=hashlib.sha256(modulepath.read_bytes()).hexdigest()
    if c.get("module_sha256") and c["module_sha256"]!=module_hash:raise ValueError("Colour module changed; review parameters before rendering")
    if not out.is_relative_to(ROOT.resolve()) or out.exists():raise ValueError("Use a fresh output inside E:/Video")
    if out.suffix.lower()!=".mkv":raise ValueError("The colour cache must be a lossless MKV")
    if pathlib.Path(str(out)+".json").exists():raise FileExistsError("Existing cache manifest")
    out.parent.mkdir(parents=True,exist_ok=True)
    import importlib.util
    sys.path.insert(0,str(modulepath.parent));spec=importlib.util.spec_from_file_location("job_colour",modulepath);gc=importlib.util.module_from_spec(spec);spec.loader.exec_module(gc)
    params=c["parameters"];missing=set(getattr(gc,"R",{}))-set(params)
    if missing:raise ValueError("Explicit parameters required; refusing inherited defaults: "+str(sorted(missing)))
    w,h=c["width"],c["height"]
    if (w,h)!=(1080,1920):raise ValueError("This adapter requires the project's 1080x1920 mask geometry")
    # A helper can load mask pixels from an external asset at import time. Its
    # Python file hash alone does not identify that asset for same-job reuse.
    mask_array=np.ascontiguousarray(gc.MASK)
    mask_identity={"shape":list(mask_array.shape),"dtype":mask_array.dtype.str,
                   "sha256":hashlib.sha256(memoryview(mask_array).cast("B")).hexdigest()}
    mode=c.get("compute","gpu");cp=None
    blur_mode=c.get("gpu_blur","prefix-fp64")
    if blur_mode not in ("prefix-fp64","local-fp64"):raise ValueError("gpu_blur must be prefix-fp64 or local-fp64")
    if blur_mode=="local-fp64" and mode!="gpu":raise ValueError("local-fp64 blur requires compute=gpu")
    if mode=="gpu":
        cp=load_cupy();gc.np=cp;gc.MASK=cp.asarray(gc.MASK)
        for name in ["luma","smoothstep","box_blur"]:
            fn=getattr(gc,name);setattr(gc,name,types.FunctionType(fn.__code__,{**fn.__globals__,"np":cp},fn.__name__,fn.__defaults__,fn.__closure__))
        # Explicit current-job opt-in only; existing configs keep prefix sums.
        if blur_mode=="local-fp64":
            from studio_blur_gpu import make_blur
            gc.box_blur=make_blur(cp)
    elif mode!="cpu":raise ValueError("compute must be cpu or gpu")
    source_identity={"path":str(src),"bytes":src.stat().st_size,"mtime_ns":src.stat().st_mtime_ns,"sha256":hash_file(src)}
    depfiles={modulepath}
    for helper in ["luma","smoothstep","box_blur"]:
        fn=getattr(gc,helper)
        file=fn.__globals__.get("__file__")
        if file and pathlib.Path(file).is_file():depfiles.add(pathlib.Path(file).resolve())
    dependencies={str(p):hash_file(p) for p in sorted(depfiles)}
    # CPU matting won the measured test on this GTX 1650; GPU arrays are reserved for colour.
    session=matting_session(gpu=False,threads=2) if params.get("wall_lift",0) else None
    identity={"source":source_identity,"configuration":{k:v for k,v in c.items() if k!="output"},"colour_dependencies":dependencies,"numpy":np.__version__,"ort":None if session is None else sys.modules["onnxruntime"].__version__,"cupy":None if cp is None else cp.__version__,"cuda_runtime":None if cp is None else cp.cuda.runtime.runtimeGetVersion(),"cuda_driver":None if cp is None else cp.cuda.runtime.driverGetVersion(),"matte_model_sha256":hash_file(ROOT/"models/rvm/rvm_mobilenetv3_fp32.onnx") if session else None,"adapter_sha256":hash_file(__file__),"python":sys.version,"ffmpeg":subprocess.check_output(["ffmpeg","-version"],text=True).splitlines()[0]}
    identity["static_mask"]=mask_identity;identity["gpu_blur"]=blur_mode
    cache_key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    rec=[np.zeros((1,1,1,1),np.float32) for _ in range(4)]
    if c["preprocess"]!="hlg-hable-bt709":raise ValueError("Unsupported preprocessing; specify a reviewed colour path")
    eb=params["exposure_ev"];ef=eb+params["face_ev"]
    fc=("[0:v]fps=30,zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,split[l1][l2];"+
        f"[l1]exposure=exposure={eb},tonemap=tonemap=hable:desat=0,zscale=t=bt709,format=gbrp16le[b];"+
        f"[l2]exposure=exposure={ef},tonemap=tonemap=hable:desat=0,zscale=t=bt709,format=gbrp16le[f];[b][f]hstack,format=gbrp16le")
    frames=int(c["frames"]);start=float(c["start"])
    if frames<1 or start<0:raise ValueError("Positive frame count and nonnegative start required")
    warm=int(c.get("matte_warmup_frames",0))
    if warm<0 or warm>round(start*30):raise ValueError("Matte warmup exceeds available earlier frames")
    strength=float(c["dither_strength"]);rng=np.random.default_rng(int(c["dither_seed"]))
    if strength<0 or strength>1/255:raise ValueError("Dither strength must be reviewed in range 0..1/255")
    info=json.loads(subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_streams","-of","json",str(src)]))["streams"][0]
    if info.get("color_transfer")!="arib-std-b67" or info.get("color_primaries")!="bt2020":raise ValueError("This reviewed preprocessing adapter requires actual HLG BT.2020 input metadata")
    decode=["ffmpeg","-nostdin","-v","error","-ss",str(start-warm/30),"-threads","2","-i",str(src),"-filter_complex",fc,"-frames:v",str(frames+warm),"-f","rawvideo","-pix_fmt","gbrp16le","pipe:1"]
    temp=out.with_name(out.stem+".partial-"+uuid.uuid4().hex[:8]+out.suffix)
    encode=["ffmpeg","-nostdin","-v","error","-n","-f","rawvideo","-pix_fmt","rgb48le","-s",f"{w}x{h}","-r","30","-i","pipe:0","-an","-c:v","ffv1","-level","3","-slicecrc","1","-pix_fmt","gbrp16le","-color_primaries","bt709","-color_trc","bt709","-colorspace","rgb","-color_range","pc",str(temp)]
    d=e=None;count=0;timing={"read":0.0,"matte":0.0,"colour":0.0,"write":0.0};allstart=time.perf_counter()
    log=pathlib.Path(str(out)+".log")
    with log.open("w",encoding="utf-8") as errors:
        try:
            d=subprocess.Popen(decode,stdout=subprocess.PIPE,stderr=errors,bufsize=0);e=subprocess.Popen(encode,stdin=subprocess.PIPE,stderr=errors)
            for frame_index in range(frames+warm):
                t=time.perf_counter();raw=read_exact(d.stdout,2*w*h*3*2)
                z=np.frombuffer(raw,"<u2").reshape(3,h,2*w)
                base=np.stack([z[2,:,:w],z[0,:,:w],z[1,:,:w]]).astype(np.float32)/65535
                face=np.stack([z[2,:,w:],z[0,:,w:],z[1,:,w:]]).astype(np.float32)/65535
                timing["read"]+=time.perf_counter()-t;alpha=None;t=time.perf_counter()
                if session:
                    feeds={"src":base[None],"downsample_ratio":np.array([min(512/max(w,h),1)],np.float32)}
                    feeds.update({f"r{i+1}i":r for i,r in enumerate(rec)})
                    fgr,pha,*rec=session.run(None,feeds);alpha=pha[0,0]
                timing["matte"]+=time.perf_counter()-t
                if frame_index<warm:continue
                t=time.perf_counter()
                if cp:
                    result=cp.asnumpy(gc.correct(cp.asarray(base),cp.asarray(face),params,c["shirt_gains"],alpha=None if alpha is None else cp.asarray(alpha)))
                else:result=gc.correct(base,face,params,c["shirt_gains"],alpha=alpha)
                timing["colour"]+=time.perf_counter()-t;t=time.perf_counter()
                if strength:result+=(rng.random(result.shape,dtype=np.float32)-.5)*strength
                pixels=(np.clip(result,0,1).transpose(1,2,0)*65535+.5).astype("<u2")
                e.stdin.write(pixels.tobytes());timing["write"]+=time.perf_counter()-t;count+=1
                if count%30==0:print(f"Processed {count}/{frames}",flush=True)
            e.stdin.close();ec=e.wait(timeout=60);dc=d.wait(timeout=60)
            if ec or dc:raise RuntimeError(f"FFmpeg decode={dc}, encode={ec}; inspect {log}")
            if src.stat().st_size!=source_identity["bytes"] or src.stat().st_mtime_ns!=source_identity["mtime_ns"]:raise RuntimeError("Source recording changed during rendering")
            if any(hash_file(p)!=digest for p,digest in dependencies.items()):raise RuntimeError("Colour dependencies changed during rendering; output not promoted")
            if out.exists():raise FileExistsError(out)
            temp.rename(out)
            result={"scope":"Actual decode + CPU matting + selected colour compute + lossless FFV1 encoding; excludes graphics/audio","compute":mode,"gpu_blur":blur_mode,"frames":count,"seconds":time.perf_counter()-allstart,"timing":timing,"config":c,"module_sha256":module_hash,"source_identity":source_identity,"cache_key":cache_key,"cache_identity":identity,"config_sha256":hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest(),"matting_provider":session.get_providers() if session else None,"lossless_cache":"16-bit RGB FFV1; preserves computed/quantised frames; not a small Instagram upload"}
            pathlib.Path(str(out)+".json").write_text(json.dumps(result,indent=2),encoding="utf-8");print(json.dumps({k:result[k] for k in ["compute","frames","seconds","timing"]}),flush=True)
        finally:
            for p in [d,e]:
                if p and p.poll() is None:p.kill();p.wait()
            if temp.exists():temp.unlink()
if __name__=="__main__":main()
