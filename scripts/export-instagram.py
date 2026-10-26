"""One video encode from an SDR master; separate true lossless archive.
Delivery presets (2026-10-25, measured on a 15 s v12 excerpt, see plans/TIMELINE-RENDERER-v1.md):
  balanced (DEFAULT)  NVENC p7 tuned CQ24  ~89 MB per 80 s, VMAF 98.4 / 47.7 dB, no visible difference in zoomed face/text/fabric crops
  max                 NVENC p7 tuned CQ20  ~151 MB per 80 s, VMAF 98.9 / 49.3 dB (only when a larger file is explicitly wanted)
CPU fallback (explicit -Encoder cpu): balanced = x264 slow CRF18 (~69 MB per 80 s, VMAF 98.3); max = x264 slow CRF16 (not separately measured).
The old untuned p4 CQ20 'high' and CQ23 'compact' presets were retired."""
import argparse,json,pathlib,subprocess,time,uuid,re
ROOT=pathlib.Path("E:/Video")
def probe(p):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)]))
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("input");ap.add_argument("output")
    ap.add_argument("--audio",help="Optional already mixed audio file")
    ap.add_argument("--frames",action="store_true",help="Input is a contiguous Remotion PNG frame directory, 1080x1920 at 30 fps")
    ap.add_argument("--encoder",choices=["nvenc","cpu"],default="nvenc")
    ap.add_argument("--quality",choices=["balanced","max"],default="balanced")
    ap.add_argument("--audio-mode",choices=["master","copy"],default="master")
    ap.add_argument("--lossless-archive",action="store_true")
    a=ap.parse_args();src=pathlib.Path(a.input).resolve();out=pathlib.Path(a.output).resolve()
    sequence=None;frame_count=None
    if a.frames:
        if not src.is_dir():raise NotADirectoryError(src)
        numbered=[]
        for p in src.glob("element-*.png"):
            match=re.fullmatch(r"element-(\d+)\.png",p.name)
            if not match:raise ValueError("Unexpected PNG frame name")
            numbered.append((int(match[1]),len(match[1]),p))
        numbered.sort()
        if not numbered or len({digits for _,digits,_ in numbered})!=1:raise ValueError("Missing frames or inconsistent number width")
        indices=[n for n,_,_ in numbered]
        if indices!=list(range(indices[0],indices[0]+len(indices))):raise ValueError("Non-contiguous frame sequence")
        if not a.audio:raise ValueError("Frame sequence requires an explicitly selected audio file")
        if a.lossless_archive:raise ValueError("Use a video master for pixel-format-preserving archival")
        frame_count=len(indices);sequence={"first":indices[0],"pattern":str(src/("element-%0"+str(numbered[0][1])+"d.png"))}
        info=probe(numbered[0][2]);v=next(s for s in info["streams"] if s["codec_type"]=="video")
        v["avg_frame_rate"]="30/1";info["format"]["duration"]=str(frame_count/30)
    else:
        if not src.is_file():raise FileNotFoundError(src)
        info=probe(src);v=next(s for s in info["streams"] if s["codec_type"]=="video")
    if not out.is_relative_to(ROOT.resolve()) or src==out or out.exists():raise ValueError("Use a fresh output inside E:/Video")
    if pathlib.Path(str(out)+".export.json").exists():raise FileExistsError("Existing output metadata")
    from fractions import Fraction
    if (v["width"],v["height"])!=(1080,1920) or Fraction(v["avg_frame_rate"])!=30:raise ValueError("Explicitly prepare a 1080x1920 30fps master first; no silent resize or frame dropping")
    if v.get("color_transfer") in ["arib-std-b67","smpte2084"] or v.get("color_space")=="bt2020nc":raise ValueError("HDR requires a reviewed SDR conversion first; refusing to tag HDR as SDR")
    if out.suffix.lower()!=(".mkv" if a.lossless_archive else ".mp4"):raise ValueError("Lossless archive uses MKV; Instagram delivery uses MP4")
    audio=pathlib.Path(a.audio).resolve() if a.audio else src
    ai=probe(audio);has_audio=any(s["codec_type"]=="audio" for s in ai["streams"])
    out.parent.mkdir(parents=True,exist_ok=True)
    temp=out.with_name(out.stem+".partial-"+uuid.uuid4().hex[:8]+out.suffix)
    duration=float(info["format"]["duration"]);audio_filter=None;measurement=None
    pre=f"asetpts=PTS-STARTPTS,apad,atrim=duration={duration},highpass=f=70,acompressor=threshold=0.1:ratio=3.5:attack=1:release=90:makeup=1"
    t=time.perf_counter()
    if has_audio and a.audio_mode=="master" and not a.lossless_archive:
        measure=subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(audio),"-map","0:a:0","-af",pre+",loudnorm=I=-14:TP=-1.7:LRA=11:print_format=json","-vn","-f","null","-"],capture_output=True,text=True,check=True)
        measurement=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',measure.stderr,re.S)[-1])
        if measurement["input_i"]=="-inf":raise ValueError("Cannot master silent audio")
        m=measurement;audio_filter=pre+f",loudnorm=I=-14:TP=-1.7:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    cmd=["ffmpeg","-nostdin","-hide_banner","-v","info","-n"]
    if sequence:cmd+=["-framerate","30","-start_number",str(sequence["first"]),"-i",sequence["pattern"]]
    else:cmd+=["-i",str(src)]
    if has_audio and audio!=src:cmd+=["-i",str(audio)]
    cmd+=["-map","0:v:0"]
    if has_audio:cmd+=["-map",("1:a:0" if audio!=src else "0:a:0")]
    if a.lossless_archive:
        cmd+=["-c:v","ffv1","-level","3","-slicecrc","1","-pix_fmt",v["pix_fmt"]]
        if has_audio:cmd+=["-c:a","flac"]
    else:
        cmd+=["-vf","scale=out_color_matrix=bt709:out_range=limited,format=yuv420p"]
        if a.encoder=="nvenc":
            cq="24" if a.quality=="balanced" else "20"
            cmd+=["-c:v","h264_nvenc","-preset","p7","-tune","hq","-rc","vbr","-cq",cq,"-b:v","0","-maxrate","24M","-bufsize","48M","-spatial-aq","1","-aq-strength","8",
                  "-temporal-aq","1","-rc-lookahead","32","-multipass","fullres","-b_ref_mode","middle","-bf","3"]
        else:cmd+=["-c:v","libx264","-preset","slow","-crf","18" if a.quality=="balanced" else "16","-maxrate","24M","-bufsize","48M"]
        cmd+=["-profile:v","high","-pix_fmt","yuv420p","-g","60","-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-movflags","+faststart"]
        if has_audio:
            if a.audio_mode=="copy":
                ac=next(s for s in ai["streams"] if s["codec_type"]=="audio")
                if ac["codec_name"]!="aac":raise ValueError("Audio copy to MP4 requires AAC; otherwise select master")
                cmd+=["-c:a","copy"]
            else:cmd+=["-af",audio_filter,"-c:a","aac","-b:a","320k","-ar","48000","-ac","2"]
    cmd+=["-t",str(duration),str(temp)]
    log=pathlib.Path(str(out)+".ffmpeg.log")
    try:
        with log.open("w",encoding="utf-8") as f:subprocess.run(cmd,stdout=f,stderr=f,check=True)
        pi=probe(temp);vo=next(s for s in pi["streams"] if s["codec_type"]=="video")
        if (vo["width"],vo["height"])!=(1080,1920):raise ValueError("Unexpected output dimensions")
        if Fraction(vo["avg_frame_rate"])!=30:raise ValueError("Unexpected output frame rate")
        if abs(float(pi["format"]["duration"])-duration)>1/30+.001:raise ValueError("Unexpected output duration")
        if a.lossless_archive and vo["pix_fmt"]!=v["pix_fmt"]:raise ValueError("Archive changed pixel format; refusing a lossless claim")
        if out.exists():raise FileExistsError(out)
        temp.rename(out)
        result={"input":str(src),"input_frame_sequence":sequence,"expected_video_frames":frame_count,"output":str(out),"seconds":round(time.perf_counter()-t,3),"bytes":out.stat().st_size,"encoder":"ffv1" if a.lossless_archive else a.encoder,"quality":a.quality,"mathematically_lossless_video":a.lossless_archive,"reference_boundary":"Decoded input frames; prior source or master compression is not undone","audio_measurement":measurement,"full_command":cmd,"output_probe":pi,"review":"Technical export completed; visual equivalence and Instagram recompression require separate assessment"}
        pathlib.Path(str(out)+".export.json").write_text(json.dumps(result,indent=2),encoding="utf-8");print(json.dumps({k:result[k] for k in ["output","seconds","bytes","encoder","mathematically_lossless_video"]}))
    except Exception:
        if temp.exists():temp.unlink()
        raise
if __name__=="__main__":main()
