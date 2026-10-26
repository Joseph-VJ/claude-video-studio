import argparse,json,os
from pathlib import Path
from faster_whisper import WhisperModel
p=argparse.ArgumentParser()
p.add_argument('input');p.add_argument('--output');p.add_argument('--model',default='small');p.add_argument('--language');p.add_argument('--prompt',default='')
a=p.parse_args()
root=Path('E:/Video');src=Path(a.input).resolve();out=Path(a.output) if a.output else root/'projects'/src.stem/'words.json'
if not src.is_file():raise SystemExit(f'Missing video: {src}')
if not out.resolve().is_relative_to(root):raise SystemExit('Output must stay under E:/Video')
model=WhisperModel(a.model,device='cpu',compute_type='int8',download_root=str(root/'models'/'whisper'),cpu_threads=4)
segments,info=model.transcribe(str(src),language=a.language,word_timestamps=True,vad_filter=True,initial_prompt=a.prompt or None)
words=[{'text':w.word.strip(),'startMs':round(w.start*1000),'endMs':round(w.end*1000)} for s in segments for w in (s.words or []) if w.word.strip()]
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(out),'language':info.language,'words':len(words),'transcript':' '.join(w['text'] for w in words)}))
