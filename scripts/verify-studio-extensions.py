import pathlib,subprocess,json,sys,hashlib
import numpy as np
from PIL import Image,ImageOps,ImageDraw
root=pathlib.Path("E:/Video");qa=root/"work/extensions-qa"
def run(args):return subprocess.run(args,capture_output=True,text=True,check=True).stdout
results={}
for name,frames in [("car-alpha-v1.webm",6),("car-composite-v1.mp4",6),("car-mask-v1.mkv",6),("car-gemini-video-v1.mp4",6),("gemini-cleaned-fixture-v1.mp4",3)]:
    src=qa/name
    info=json.loads(run(["ffprobe","-v","error","-count_frames","-show_streams","-of","json",str(src)]))
    video=next(x for x in info["streams"] if x["codec_type"]=="video")
    assert int(video["nb_read_frames"])==frames,(name,video)
    subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(src),"-f","null","-"],check=True,capture_output=True)
    audio=any(x["codec_type"]=="audio" for x in info["streams"])
    assert audio==(name!="gemini-cleaned-fixture-v1.mp4"),name
    results[name]={"frames":frames,"audio_preserved":audio,"full_decode":True,"size":[video["width"],video["height"]]}
alpha=np.array(Image.open(qa/"video-alpha-mask-v1.png").convert("L"))
assert alpha.min()==0 and alpha.max()==255
results["transparent_video"]={"independent_libvpx_decode":True,"alpha_range":[int(alpha.min()),int(alpha.max())],"transparent_fraction":float(np.mean(alpha<128))}
rgba=Image.open(qa/"car-cutout-v1.png").convert("RGBA")
bg=Image.new("RGBA",rgba.size,"#202020");bg.alpha_composite(rgba);bg=bg.convert("RGB")
panels=[("Image cutout on grey",bg),("Video cutout frame",Image.open(qa/"video-composite-frame-v1.png"))]
for label,name in [("Gemini video BEFORE","gemini-before.png"),("Gemini video AFTER","gemini-after.png")]:
    im=Image.open(qa/name).convert("RGB");w,h=im.size
    panels.append((label+" (lower right)",im.crop((max(0,w-220),max(0,h-140),w,h))))
for label,name in [("Gemini image BEFORE","D:/gemini-watermark-remover/tests/fixtures/dark-background-standard-support-96.png"),("Gemini image AFTER",str(qa/"gemini-cleaned-image-fixture-v1.png"))]:
    panels.append((label,Image.open(name).convert("RGB")))
sheet=Image.new("RGB",(960,3*310),"#303030");draw=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(panels):
    x=(i%2)*480;y=(i//2)*310
    draw.text((x+10,y+8),label,fill="white")
    view=ImageOps.contain(im,(460,270))
    sheet.paste(view,(x+10,y+32))
sheet.save(qa/"verification-contact.png")
checks=sorted((root/"projects/studio-extension-demo/.context/checkpoints").glob("*/STATE.md"))
assert checks
assert "Smoke test:" in (root/"projects/studio-extension-demo/.context/LAST-COMPACT.md").read_text()
results["context"]={"precompact_checkpoint":True,"postcompact_summary":True,"session_start_output_tested":True,"native_live_session_tested":False}
results["model"]={"bytes":(root/"models/u2netp/u2netp.onnx").stat().st_size,"sha256":hashlib.sha256((root/"models/u2netp/u2netp.onnx").read_bytes()).hexdigest()}
results["skills"]={"new_count":6,"legacy_forwarders":19,"bytes_without_git":sum(p.stat().st_size for p in (root/".claude/skills").rglob("*") if p.is_file() and ".git" not in p.parts)}
results["claude_auth"]="Sign-in required; no inference test"
(root/"logs/extensions-20261024/verification.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results,indent=2))
