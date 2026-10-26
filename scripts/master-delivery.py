"""Audio-only delivery master: preserves an already normalised H.264 video stream."""
import argparse, json, re, subprocess
from fractions import Fraction
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("input"); p.add_argument("output"); p.add_argument("--no-compress",action="store_true")
a=p.parse_args()
src=Path(a.input).resolve(); out=Path(a.output).resolve(); root=Path("E:/Video").resolve()
if not out.is_relative_to(root) or src==out or out.exists(): raise SystemExit("Choose a new output under E:/Video")
probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(src)],text=True))
v=next(s for s in probe["streams"] if s["codec_type"]=="video")
if (v["codec_name"],v["width"],v["height"],v["pix_fmt"])!=("h264",1080,1920,"yuv420p"):
 raise SystemExit("Normalise picture explicitly before audio-only mastering")
if Fraction(v["avg_frame_rate"])!=30: raise SystemExit("Delivery picture must be 30 fps")
duration_value=v.get("duration") or probe.get("format",{}).get("duration")
if duration_value in (None,"N/A"): raise SystemExit("Cannot establish video duration")
dur=float(duration_value)
pre=f"asetpts=PTS-STARTPTS,apad,atrim=duration={dur}"
if not a.no_compress: pre+=",acompressor=threshold=0.05:ratio=6:attack=0.1:release=80:makeup=1"
cmd=["ffmpeg","-hide_banner","-nostdin","-i",str(src)]
measure=subprocess.run(cmd+["-af",pre+",loudnorm=I=-14:TP=-1.7:LRA=11:print_format=json","-vn","-f","null","-"],capture_output=True,text=True,check=True)
m=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',measure.stderr,re.S)[-1])
if m["input_i"]=="-inf": raise SystemExit("No measurable programme audio")
f=pre+f",loudnorm=I=-14:TP=-1.7:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
out.parent.mkdir(parents=True,exist_ok=True)
subprocess.run(cmd+["-n","-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f,"-t",str(dur),"-ar","48000","-ac","2","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)],capture_output=True,text=True,check=True)
print(json.dumps({"output":str(out),"duration":dur,"videoStreamCopied":True,"targetLufs":-14,"targetTruePeak":-1.7}))
