"""Experimental monotonic FFV1 chunk assembly. Fresh files only; no production promotion.
Job fields: chunks[{path,start_frame,frames}],segments_path,audio_input,output,
source_frame_policy='edl-rounded',camera_handling='downstream'.
--execute encodes; default writes a plan. --encoder ffv1-test preserves RGB16.
"""
import argparse,json,subprocess,time,re
from pathlib import Path
ROOT=Path('E:/Video').resolve()
def path(v):
 p=Path(v).resolve()
 if not p.is_relative_to(ROOT): raise ValueError('Path outside E:/Video: '+str(p))
 return p
def probe(p,count=False):
 cmd=['ffprobe','-v','error']+(['-count_frames'] if count else [])
 return json.loads(subprocess.check_output(cmd+['-show_streams','-show_format','-of','json',str(p)],text=True,encoding='utf-8'))
def run(cmd,log):
 with log.open('w',encoding='utf-8') as f: subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('job');ap.add_argument('--execute',action='store_true');ap.add_argument('--encoder',choices=['cpu','nvenc','ffv1-test'],default='cpu');a=ap.parse_args()
 j=json.loads(path(a.job).read_text(encoding='utf-8-sig'));out=path(j['output'])
 if j.get('source_frame_policy')!='edl-rounded' or j.get('camera_handling')!='downstream': raise ValueError('Explicit frame/camera policies required')
 if out.exists(): raise FileExistsError(out)
 if out.suffix.lower()!=('.mkv' if a.encoder=='ffv1-test' else '.mp4'): raise ValueError('Wrong output suffix')
 segs=json.loads(path(j['segments_path']).read_text(encoding='utf-8-sig'));cursor=0;chunks=[];geometry=None;identities=[]
 for c in j['chunks']:
  p=path(c['path']);s=next(s for s in probe(p)['streams'] if s['codec_type']=='video');g=(s['width'],s['height'],s['pix_fmt'])
  if int(c['start_frame'])!=cursor or int(c['frames'])<=0: raise ValueError('Noncontiguous source chunks')
  if s['codec_name']!='ffv1' or s['r_frame_rate']!='30/1' or g[2]!='gbrp16le' or float(s.get('start_time',0))!=0: raise ValueError('Expected zero-start 30fps RGB16 FFV1 cache')
  if geometry and geometry!=g: raise ValueError('Different chunk formats')
  geometry=g;chunks.append((p,int(c['frames'])));cursor+=int(c['frames']);st=p.stat();identities.append({'path':str(p),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns,'identity_limit':'Stat identity; cache receipt/source/grade identity must also be reviewed'})
 ranges=[];total=0;end_previous=0
 for i,s in enumerate(segs):
  first=round(float(s['in'])*30);n=round((float(s['out'])-float(s['in']))*30);last=first+n
  if first<end_previous or n<=0 or n!=int(s['frames']) or last>cursor or int(s.get('frame',total))!=total: raise ValueError('Unsupported nonmonotonic/invalid EDL at '+str(i))
  ranges.append((first,last));end_previous=last;total+=n
 if total<=0: raise ValueError('Empty EDL')
 audio=path(j['audio_input']) if j.get('audio_input') else None
 if audio and j.get('audio_timeline')!='source-sample-zero': raise ValueError('Explicit audio_timeline=source-sample-zero required')
 if not audio and not j.get('video_only_test'): raise ValueError('Approved audio source required')
 work=out.parent/(out.stem+'-assembly');work.mkdir(parents=True,exist_ok=False)
 concat=work/'source.ffconcat';lines=['ffconcat version 1.0']
 for p,n in chunks:
  q=p.as_posix().replace("'","'\\''");lines += ["file '"+q+"'",f'duration {n/30:.12f}']
 concat.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 select='+'.join(f'between(n\\,{lo}\\,{hi-1})' for lo,hi in ranges)
 vf=f'[0:v]metadata=mode=print:key=lavf.concatdec.start_time,select={select},setpts=N/(30*TB)'
 if a.encoder!='ffv1-test': vf+=',scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p'
 filters=[vf+'[v]']
 if audio:
  filters += [f'[1:a]aresample=48000,asplit={len(segs)}'+''.join(f'[a{i}]' for i in range(len(segs)))]
  for i,s in enumerate(segs):
   start=round(float(s['in'])*48000);samples=int(s['frames'])*1600;dur=samples/48000
   filters += [f'[a{i}]atrim=start_sample={start}:end_sample={start+samples},asetpts=PTS-STARTPTS,apad,atrim=end_sample={samples},afade=t=in:d=0.006,afade=t=out:st={max(0,dur-.006):.9f}:d=0.006[b{i}]']
  filters += [''.join(f'[b{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,atrim=end_sample={total*1600},asetpts=PTS-STARTPTS[a]']
 fp=work/'filters.txt';fp.write_text(';\n'.join(filters),encoding='utf-8')
 cmd=['ffmpeg','-hide_banner','-nostdin','-n','-v','info','-segment_time_metadata','1','-f','concat','-safe','0','-i',str(concat)]
 if audio:cmd+=['-i',str(audio)]
 cmd+=['-filter_complex_script',str(fp),'-map','[v]','-fps_mode','passthrough']
 if a.encoder=='ffv1-test':cmd+=['-c:v','ffv1','-level','3','-pix_fmt','gbrp16le']
 elif a.encoder=='cpu':cmd+=['-c:v','libx264','-threads','2','-preset','fast','-crf','8','-g','30','-keyint_min','30','-pix_fmt','yuv420p']
 else:cmd+=['-c:v','h264_nvenc','-preset','p4','-tune','hq','-rc','vbr','-cq','16','-b:v','0','-g','30','-pix_fmt','yuv420p']
 if a.encoder!='ffv1-test':cmd+=['-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-movflags','+faststart']
 if audio:
  cmd+=['-map','[a]','-c:a','pcm_s16le' if a.encoder=='ffv1-test' else 'aac','-ar','48000']
  if a.encoder!='ffv1-test':cmd+=['-b:a','192k']
 cmd+=[str(out)];report={'status':'plan-only','job':j,'frames':total,'ranges':ranges,'cache_stat_identities':identities,'command':cmd,'limits':['Experimental; not promoted to production','Source frames map from rounded EDL; legacy joined video had AAC-induced 21ms offset','No grading, camera, graphics or final audio mastering performed']};rp=work/'assembly.json';rp.write_text(json.dumps(report,indent=2),encoding='utf-8')
 if a.execute:
  t=time.perf_counter();run(cmd,work/'encode.log');report['encode_seconds']=time.perf_counter()-t
  groups={}
  for key in re.findall(r'lavf\.concatdec\.start_time=(-?\d+)',(work/'encode.log').read_text(encoding='utf-8',errors='replace')):groups[key]=groups.get(key,0)+1
  report['decoded_chunk_frames']=list(groups.values())
  if list(groups.values())!=[n for _,n in chunks]:
   report['status']='failed-source-frame-count';rp.write_text(json.dumps(report,indent=2),encoding='utf-8');raise RuntimeError('Decoded chunk counts differ from declared source-frame map: '+str(groups))
  m=probe(out,count=a.encoder=='ffv1-test');v=next(s for s in m['streams'] if s['codec_type']=='video');count=int(v.get('nb_frames',v.get('nb_read_frames',-1)))
  if count!=total or v['avg_frame_rate']!='30/1':raise RuntimeError(f'Frame validation failed: {count}/{total}')
  run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-i',str(out),'-f','null','-'],work/'decode.log');report.update(status='technical-validation-passed',output_probe=m,bytes=out.stat().st_size,qa_limit='No subjective playback or legacy parity implied');rp.write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({'status':report['status'],'report':str(rp),'frames':total,'encode_seconds':report.get('encode_seconds')}))
if __name__=='__main__':main()
