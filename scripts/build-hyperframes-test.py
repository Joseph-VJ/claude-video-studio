from pathlib import Path
import json,html
root=Path('E:/Video/projects/hyperframes-test')
words=json.loads(Path('E:/Video/projects/test-words.json').read_text(encoding='utf-8-sig'))
clips=[];anim=[]
for i,w in enumerate(words):
 start=w['startMs']/1000;duration=max(.12,(w['endMs']-w['startMs'])/1000)
 clips.append(f'<div class="clip caption" id="word-{i}" data-start="{start}" data-duration="{duration}" data-track-index="2"><span id="text-{i}">{html.escape(w["text"])}</span></div>')
 anim.append(f'tl.fromTo("#text-{i}",{{scale:.82}},{{scale:1,duration:.12,ease:"power2.out"}},{start});')
s='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920"><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:LocalArial;src:url('assets/fonts/ArialBold.ttf') format('truetype');font-weight:700 900}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#102030;font-family:LocalArial,sans-serif}
#root{position:relative;width:100%;height:100%;overflow:hidden}
#footage{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0;background:rgba(8,18,32,.74)}
.headline{position:absolute;left:90px;right:120px;top:300px;color:#fff;font-size:86px;line-height:1.12;z-index:2}
.caption{position:absolute;left:90px;right:120px;top:1180px;height:180px;display:flex;align-items:center;justify-content:center;z-index:3}
.caption span{display:block;padding:22px 42px;border-radius:22px;background:#e6ff63;color:#102030;font-size:86px;line-height:1.1;font-weight:700}
</style></head><body><div id="root" data-composition-id="main" data-duration="5" data-width="1080" data-height="1920" data-fps="30">
<video id="footage" class="clip" src="assets/setup-test.mp4" playsinline data-has-audio="true" data-start="0" data-duration="5" data-track-index="0"></video><div class="shade"></div>
<h1 id="headline" class="clip headline" data-start="0" data-duration="5" data-track-index="1">HyperFrames<br>Local render test</h1>
__CLIPS__</div><script>const tl=gsap.timeline({paused:true});__ANIM__ window.__timelines['main']=tl;</script></body></html>'''
s=s.replace('HyperFrames<br>Local render test','HyperFrames local render test.').replace('__CLIPS__','\n'.join(clips)).replace('__ANIM__','\n'.join(anim))
(root/'index.html').write_text(s,encoding='utf-8')
(root/'package.json').write_text(json.dumps({'name':'hyperframes-test','private':True,'type':'module','scripts':{'dev':'hyperframes preview','check':'hyperframes check','render':'hyperframes render'}}),encoding='utf-8')
