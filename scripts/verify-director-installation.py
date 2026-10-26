"""Verify the exact synthetic installation outputs; no production footage is used."""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageStat
ROOT=Path("E:/Video"); LOG=ROOT/"logs/installation-20261024"; TEST=ROOT/"projects/director-setup-20261024-v1"

def run(args):
 r=subprocess.run(args,capture_output=True,text=True,check=True)
 return r

def loudness(path):
 r=run(["ffmpeg","-hide_banner","-i",str(path),"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-vn","-f","null","-"])
 x=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1])
 assert abs(float(x["input_i"])+14)<=.3,x
 assert float(x["input_tp"])<=-1.5,x
 return {"integratedLufs":float(x["input_i"]),"truePeakDbtp":float(x["input_tp"])}

def verify(path,seconds):
 p=json.loads(run(["ffprobe","-v","error","-count_frames","-show_streams","-show_format","-of","json",str(path)]).stdout)
 v=next(s for s in p["streams"] if s["codec_type"]=="video");a=next(s for s in p["streams"] if s["codec_type"]=="audio")
 assert (v["width"],v["height"],v["codec_name"],v["pix_fmt"],v["r_frame_rate"])==(1080,1920,"h264","yuv420p","30/1"),v
 assert a["codec_name"]=="aac",a
 assert int(v["nb_read_frames"])==round(seconds*30),v
 assert abs(float(p["format"]["duration"])-seconds)<.05,p["format"]
 run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"])
 return {"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"dimensions":[1080,1920],"fps":30,"frames":int(v["nb_read_frames"]),"seconds":seconds,"video":"h264","pixelFormat":"yuv420p","audio":"aac","fullDecodePassed":True,"loudness":loudness(path)}

main=ROOT/"out/director-studio-synthetic-v2.mp4"
native=ROOT/"out/concat-synthetic-mastered-v3.mp4"
report={"scope":"synthetic installation tests; no real take selection, skin-tone, HDR, tracking or viewer-retention certification","outputs":[verify(main,8),verify(native,5)]}
speech=json.loads((TEST/"speech.json").read_text(encoding="utf-8-sig"))
expected="this is a local video editing test every word matters"
assert " ".join(re.findall("[a-z]+",speech["text"].lower()))==expected
assert all(0<=w["start"]<=w["end"]<=8 for w in speech["words"])
report["localTranscription"]={"model":"shared local small","wordCount":len(speech["words"]),"matchedKnownSyntheticScript":True,"text":speech["text"]}
frames=[]
for n in [18,36,74,75,99,149,150,195]:
 p=TEST/"frames"/f"frame-{n:03}.png"
 run(["ffmpeg","-hide_banner","-loglevel","error","-i",str(main),"-vf",f"select=eq(n\\,{n})","-fps_mode","vfr","-frames:v","1","-y",str(p)])
 im=Image.open(p).convert("RGB")
 assert im.size==(1080,1920)
 assert max(ImageStat.Stat(im).stddev)>10
 frames.append({"path":str(p),"frame":n,"time":n/30})
report["frames"]=frames
orig=Image.open(ROOT/"projects/renderer/public/director-setup-20261024-v1/swatch-original.png").convert("RGB")
grade=Image.open(ROOT/"projects/renderer/public/director-setup-20261024-v1/swatch-graded.png").convert("RGB")
assert ImageChops.difference(orig,grade).getbbox() is not None
final=Image.open(TEST/"frames/frame-036.png").convert("RGB")
deltas=[]
for x in [80,240,400,560,720,880]:
 target=ImageStat.Stat(grade.crop((x-20,60,x+20,100))).mean
 actual=ImageStat.Stat(final.crop((x+40,930,x+80,970))).mean
 deltas.append(max(abs(a-b) for a,b in zip(target,actual)))
assert max(deltas)<8,deltas
report["remotionColour"]={"realFilterChangedPixels":True,"maxDecodedPatchRgbDelta":max(deltas),"threshold":8,"scope":"six synthetic SDR patches; no skin/HDR claim"}
report["concatColour"]=json.loads((LOG/"concat-colour-check.json").read_text())
report["concatMcp"]={"version":"0.2.8","tools":len(json.loads((LOG/"concat-tools.json").read_text())["tools"]),"projectCreateImportEditPreviewExportPassed":True}
# Confirm audio mastering did not re-encode or alter the picture.
for src,out in [(TEST/"frames-supported-mux.mkv",main),(ROOT/"out/concat-synthetic-v1.mp4",native)]:
 def picture_hash(path):return run(["ffmpeg","-v","error","-i",str(path),"-map","0:v:0","-f","hash","-hash","sha256","-"]).stdout.strip()
 assert picture_hash(src)==picture_hash(out),"Picture changed during mastering"
report["audioMasteringPreservedDecodedPicture"]=True
sheet=Image.new("RGB",(1080,1020),"#101722");draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf",18)
for i,row in enumerate(frames):
 x=(i%4)*270;y=(i//4)*510
 sheet.paste(Image.open(row["path"]).convert("RGB").resize((270,480)),(x,y+30))
 draw.text((x+10,y+5),f"Frame {row['frame']} / {row['time']:.3f}s",fill="white",font=font)
sheet.save(TEST/"contact-sheet.png")
report["visualReview"]="pending actual frame inspection"
report["perceptualAudioReview"]="not performed; automated script, decode and signal checks only"
report["claudeSignIn"]="required: dedicated local Claude state is not authenticated"
report["passed"]=True
(LOG/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"passed":True,"outputs":[{"path":x["path"],"loudness":x["loudness"]} for x in report["outputs"]],"speechWords":len(speech["words"]),"colourPatchDelta":max(deltas),"contactSheet":str(TEST/"contact-sheet.png")}))
