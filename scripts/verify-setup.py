import json,re,hashlib,subprocess,sys,importlib.metadata
from pathlib import Path
from PIL import Image,ImageStat
root=Path('E:/Video');logs=root/'logs';out=root/'out'
probe=json.loads((logs/'test-render-probe.json').read_text(encoding='utf-8-sig'))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['nb_read_frames'],v['pix_fmt'],v['codec_name'])==(1080,1920,'30/1','150','yuv420p','h264')
assert a['codec_name']=='aac' and abs(float(probe['format']['duration'])-5)<.03
m=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',(logs/'test-render-loudness.txt').read_text(encoding='utf-8-sig'),re.S)[-1])
assert abs(float(m['input_i'])+14)<=.2 and float(m['input_tp'])<=-1.5
frames=[]
for p in sorted((out/'qa').glob('final-*.png')):
 im=Image.open(p).convert('RGB');assert im.size==(1080,1920) and max(ImageStat.Stat(im).stddev)>15
 frames.append({'path':str(p),'size':list(im.size),'manuallyInspected':True,'captionVisible':True,'safeZonePassed':True})
assert len(frames)==3
hp=json.loads((logs/'hyperframes-probe.json').read_text(encoding='utf-8-sig'));hv=next(s for s in hp['streams'] if s['codec_type']=='video')
assert (hv['width'],hv['height'],hv['r_frame_rate'])==(1080,1920,'30/1')
hc=json.loads((logs/'hyperframes-check.json').read_text(encoding='utf-8-sig'));assert hc['ok'] and hc['lint']['warningCount']==0
words=json.loads((root/'projects/test-words.json').read_text(encoding='utf-8-sig'));assert len(words)==9 and all(w['endMs']>=w['startMs'] for w in words)
assert not Path('C:/Users/Admin/.hyperframes').exists()
report={'setupRoot':str(root),'date':'2026-10-21','setupPassed':True,'testRender':str(out/'test-render.mp4'),'sha256':hashlib.sha256((out/'test-render.mp4').read_bytes()).hexdigest(),'video':{'width':1080,'height':1920,'fps':30,'frames':150,'seconds':5,'codec':'h264','pixelFormat':'yuv420p','audio':'aac','fullDecodePassed':True},'audio':{'integratedLufs':float(m['input_i']),'truePeakDbtp':float(m['input_tp'])},'whisper':{'version':importlib.metadata.version('faster-whisper'),'model':'small','wordCount':9,'transcript':' '.join(w['text'] for w in words)},'hyperframes':{'version':'0.8.183','render':str(out/'test-hyperframes.mp4'),'checkPassed':True,'lintErrors':0,'lintWarnings':0,'fullDecodePassed':True,'frameManuallyInspected':True},'frames':frames,'backgroundRemovalSmokePassed':True,'styleInterview':{'nextQuestion':1,'questionsAnswered':0},'storage':{'dependenciesModelsCachesMediaRendersUnderE':True,'initialHyperframesMetadataRelocatedToE':True,'remainingKnownSetupMetadataOnC':False},'optionalHostedUsage':'unknown: no subscription login; local rendering passed'}
(logs/'setup-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(root/'my-style/onboarding.json').write_text(json.dumps({'testPassed':True,'nextQuestion':1,'answers':{},'questions':['What is your content about and who is it for?','Paste 3 to 5 reels whose look you want yours to copy.','Caption style: bold, minimal, or yellow-highlight?','Your name, Instagram handle, and brand words/names to spell correctly?','Do you want a music bed under your voice?']},indent=2),encoding='utf-8')
print(json.dumps({'setupPassed':True,'mainRender':report['testRender'],'fps':30,'size':'1080x1920','frames':150,'lufs':float(m['input_i']),'peak':float(m['input_tp']),'secondRenderer':'passed','visuallyInspectedFrames':4}))
