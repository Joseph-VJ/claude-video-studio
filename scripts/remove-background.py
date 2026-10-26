"""Local image cutouts and recurrent person-video matting.
U2NETP preprocessing adapted from rembg (MIT); RVM API follows its GPL-3.0 docs.
See E:/Video/tools/background-removal/NOTICE.md and LICENSE-rembg.txt.
"""
import argparse, json, os, pathlib, subprocess, shutil, time, uuid, hashlib
from fractions import Fraction
ROOT=pathlib.Path("E:/Video")
for k,v in {"TEMP":"cache/tmp","TMP":"cache/tmp","TMPDIR":"cache/tmp","XDG_CACHE_HOME":"cache/xdg"}.items():
    os.environ[k]=str(ROOT/v)
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageOps, ImageColor
MODEL=ROOT/"models/u2netp/u2netp.onnx"
class Segmenter:
    def __init__(self):
        if hashlib.md5(MODEL.read_bytes()).hexdigest()!="8e83ca70e441ab06c318d82300c84806": raise ValueError("U2NETP model checksum mismatch")
        opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(MODEL),sess_options=opts,providers=["CPUExecutionProvider"])
        self.key=self.session.get_inputs()[0].name
    def mask(self,img):
        ar=np.asarray(img.convert("RGB").resize((320,320),Image.Resampling.LANCZOS),dtype=np.float32)
        ar=ar/max(float(ar.max()),1e-6)
        ar=(ar-np.array([.485,.456,.406],dtype=np.float32))/np.array([.229,.224,.225],dtype=np.float32)
        pred=self.session.run(None,{self.key:ar.transpose(2,0,1)[None,...].astype(np.float32)})[0][0,0]
        lo,hi=float(pred.min()),float(pred.max())
        pred=(pred-lo)/max(hi-lo,1e-6)
        return Image.fromarray((np.clip(pred,0,1)*255).astype(np.uint8)).resize(img.size,Image.Resampling.LANCZOS)
class PersonMatting:
    def __init__(self):
        path=ROOT/"models/rvm/rvm_mobilenetv3_fp32.onnx"
        if hashlib.sha256(path.read_bytes()).hexdigest()!="88d4531297118f595bf2fd60f6f566aec2e559393802d1f436c380f0cbbd2828": raise ValueError("RVM model differs from the pinned installation hash")
        opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(path),sess_options=opts,providers=["CPUExecutionProvider"])
        self.rec=[np.zeros((1,1,1,1),dtype=np.float32) for _ in range(4)]
        self.foreground=None
    def mask(self,img):
        rgb=np.asarray(img.convert("RGB"),dtype=np.float32)/255
        feeds={"src":rgb.transpose(2,0,1)[None,...],"downsample_ratio":np.array([min(512/max(img.size),1.0)],dtype=np.float32)}
        feeds.update({f"r{i+1}i":r for i,r in enumerate(self.rec)})
        fgr,pha,*self.rec=self.session.run(None,feeds)
        self.foreground=(np.clip(fgr[0].transpose(1,2,0),0,1)*255).astype(np.uint8)
        return Image.fromarray((np.clip(pha[0,0],0,1)*255).astype(np.uint8))

def binary(name):
    found=shutil.which(name)
    if found:return found
    fallback=pathlib.Path("C:/Users/Admin/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin")/(name+".exe")
    if fallback.exists():return str(fallback)
    raise FileNotFoundError("Load E:/Video/scripts/env.ps1; missing "+name)
def probe(src):
    return json.loads(subprocess.check_output([binary("ffprobe"),"-v","error","-show_streams","-show_format","-of","json",str(src)]))
def target(path):
    p=pathlib.Path(path).resolve()
    if not p.is_relative_to(ROOT.resolve()):raise ValueError("Output must be inside E:/Video")
    if p.exists() or pathlib.Path(str(p)+".qa.json").exists(): raise FileExistsError("Use a fresh output filename")
    p.parent.mkdir(parents=True,exist_ok=True)
    return p
def full_read(stream,n):
    data=bytearray()
    while len(data)<n:
        chunk=stream.read(n-len(data))
        if not chunk:break
        data.extend(chunk)
    if data and len(data)!=n:raise RuntimeError("Truncated decoded frame")
    return data
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="command",required=True)
    for name in ["image","video"]:
        p=sub.add_parser(name);p.add_argument("--input",required=True);p.add_argument("--output",required=True)
    v=sub.choices["video"];v.add_argument("--mode",choices=["composite","alpha","mask"],default="composite")
    v.add_argument("--model",choices=["rvm","u2netp"],default="rvm",help="rvm: recurrent people matting; u2netp: general salient objects")
    v.add_argument("--background",default="#202020");v.add_argument("--fps",type=float,default=30)
    v.add_argument("--max-side",type=int,default=1280);v.add_argument("--seconds",type=float);v.add_argument("--start",type=float,default=0)
    a=ap.parse_args();src=pathlib.Path(a.input).resolve()
    if not src.is_file():raise FileNotFoundError(src)
    out=target(a.output);pending=out.with_name(out.stem+".partial-"+uuid.uuid4().hex[:8]+out.suffix)
    start=time.monotonic();model_name=a.model if a.command=="video" else "u2netp"
    model=PersonMatting() if model_name=="rvm" else Segmenter()
    evidence={"source":str(src),"output":str(out),"model":model_name,"provider":"CPUExecutionProvider","quality_review":"Pending visual inspection on actual content","temporal_model":model_name=="rvm"}
    try:
        if a.command=="image":
            if out.suffix.lower()!=".png":raise ValueError("Image cutout output must be PNG")
            with Image.open(src) as opened:img=ImageOps.exif_transpose(opened).convert("RGBA")
            m=np.asarray(model.mask(img),dtype=np.uint16)
            old=np.asarray(img.getchannel("A"),dtype=np.uint16)
            img.putalpha(Image.fromarray(((m*old)//255).astype(np.uint8)))
            img.save(pending,format="PNG")
            evidence.update(size=img.size,alpha_range=img.getchannel("A").getextrema())
        else:
            if a.fps<=0 or a.fps>120 or a.max_side<32 or a.start<0 or (a.seconds is not None and a.seconds<=0):raise ValueError("Invalid fps, size, start or duration")
            suffix={"composite":".mp4","alpha":".webm","mask":".mkv"}[a.mode]
            if out.suffix.lower()!=suffix:raise ValueError("Mode requires "+suffix)
            info=probe(src);stream=next(x for x in info["streams"] if x["codec_type"]=="video")
            if stream.get("color_transfer") in ["smpte2084","arib-std-b67"]:raise ValueError("Normalize HDR to SDR before segmentation")
            w,h=stream["width"],stream["height"]
            rotation=next((x.get("rotation",0) for x in stream.get("side_data_list",[]) if "rotation" in x),0)
            if abs(int(rotation))%180==90:w,h=h,w
            factor=min(1,a.max_side/max(w,h));w=max(2,int(w*factor)//2*2);h=max(2,int(h*factor)//2*2)
            ff=binary("ffmpeg");trim=["-ss",str(a.start),"-i",str(src)]
            dur=["-t",str(a.seconds)] if a.seconds else []
            decode=[ff,"-nostdin","-v","error",*trim,*dur,"-an","-vf",f"scale={w}:{h},fps={a.fps},format=rgb24","-f","rawvideo","pipe:1"]
            pix={"alpha":"rgba","mask":"gray","composite":"rgb24"}[a.mode]
            encode=[ff,"-nostdin","-v","error","-n","-f","rawvideo","-pix_fmt",pix,"-s",f"{w}x{h}","-r",str(a.fps),"-i","pipe:0",*trim,"-map","0:v:0","-map","1:a:0?"]
            if a.mode=="alpha":encode+=["-c:v","libvpx-vp9","-pix_fmt","yuva420p","-auto-alt-ref","0","-crf","28","-b:v","0","-c:a","libopus","-b:a","128k"]
            elif a.mode=="mask":encode+=["-c:v","ffv1","-pix_fmt","gray","-c:a","flac"]
            else:encode+=["-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart"]
            encode+=["-shortest",*dur,str(pending)]
            dec=enc=None;count=0;amin=255;amax=0
            log=pathlib.Path(str(out)+".ffmpeg.log")
            with log.open("wb") as errors:
                try:
                    dec=subprocess.Popen(decode,stdout=subprocess.PIPE,stderr=errors)
                    enc=subprocess.Popen(encode,stdin=subprocess.PIPE,stderr=errors)
                    bg=np.array(ImageColor.getrgb(a.background),dtype=np.float32)
                    while True:
                        raw=full_read(dec.stdout,w*h*3)
                        if not raw:break
                        rgb=np.frombuffer(raw,dtype=np.uint8).reshape(h,w,3)
                        mask=np.asarray(model.mask(Image.fromarray(rgb)),dtype=np.uint8)
                        amin=min(amin,int(mask.min()));amax=max(amax,int(mask.max()))
                        if model_name=="rvm":rgb=model.foreground
                        if a.mode=="mask":frame=mask
                        elif a.mode=="alpha":frame=np.dstack([rgb,mask])
                        else:
                            alpha=mask.astype(np.float32)[...,None]/255
                            frame=np.clip(rgb*alpha+bg*(1-alpha),0,255).astype(np.uint8)
                        enc.stdin.write(frame.tobytes());count+=1
                        if count%30==0:print(f"Processed {count} frames",flush=True)
                    enc.stdin.close()
                    dr=dec.wait(timeout=60);er=enc.wait(timeout=60)
                    if dr or er or not count:raise RuntimeError(f"FFmpeg failed or empty clip: decode={dr}, encode={er}; see {log}")
                finally:
                    for proc in [dec,enc]:
                        if proc and proc.poll() is None:proc.kill();proc.wait()
            evidence.update(mode=a.mode,size=[w,h],frames=count,fps=a.fps,start_seconds=a.start,alpha_range=[amin,amax],output_probe=probe(pending),framewise_flicker_risk=model_name=="u2netp")
        if out.exists():raise FileExistsError(out)
        pending.rename(out)
        evidence["elapsed_seconds"]=round(time.monotonic()-start,3)
        pathlib.Path(str(out)+".qa.json").write_text(json.dumps(evidence,indent=2),encoding="utf-8")
        print(json.dumps({"output":str(out),"elapsed_seconds":evidence["elapsed_seconds"],"alpha_range":evidence["alpha_range"]}))
    except Exception:
        if pending.exists():pending.unlink()
        raise
if __name__=="__main__":main()
