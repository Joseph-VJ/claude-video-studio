import React from 'react';
import {AbsoluteFill,Audio,Composition,Img,registerRoot,staticFile,useCurrentFrame,spring} from 'remotion';
import transcript from './director-setup-words.json';
const F: React.FC=()=>{
 const f=useCurrentFrame(), t=f/30;
 const active=transcript.words.find(w=>t>=w.start&&t<w.end);
 const phase=f<75?0:f<150?1:2;
 const step=['Understand the content','Plan for the viewer','Check the delivered file'][phase];
 const pop=active?spring({frame:f-Math.round(active.start*30),fps:30,config:{damping:18,stiffness:220}}):1;
 return <AbsoluteFill style={{backgroundColor:['#101d2d','#1c2838','#102c2a'][phase],color:'#f3f5f7',fontFamily:'Arial, sans-serif'}}>
  <Audio src={staticFile('director-setup-20261024-v1/speech.wav')}/>
  <div style={{position:'absolute',left:60,right:100,top:270,fontSize:30,letterSpacing:5,color:'#c6e6a3'}}>VJ / LOCAL DIRECTOR STUDIO</div>
  <div style={{position:'absolute',left:60,right:100,top:370,fontSize:104,fontWeight:900,lineHeight:1.08}}>Understand.<br/>Plan.<br/><span style={{color:'#d6f582'}}>Make it clear.</span></div>
  <div style={{position:'absolute',left:60,right:100,top:780,fontSize:30,color:'#aebfc9'}}>SYNTHETIC COLOUR ROUND-TRIP</div>
  <Img src={staticFile('director-setup-20261024-v1/swatch-graded.png')} style={{position:'absolute',left:60,top:870,width:960,height:160}}/>
  <div style={{position:'absolute',left:60,right:100,top:1080,fontSize:39,fontWeight:700}}>{'0'+(phase+1)} / {step}</div>
  <div style={{position:'absolute',left:60,right:100,top:1200,height:155,display:'flex',alignItems:'center',justifyContent:'center'}}>
   {active?<span style={{fontSize:84,fontWeight:900,color:'#132333',background:'#d6f582',padding:'18px 35px',borderRadius:16,transform:'scale('+(.92+.08*pop)+')'}}>{active.text}</span>:<span style={{fontSize:30,color:'#aebfc9'}}>SPEECH · CAPTIONS · COLOUR · SOUND</span>}
  </div>
  <div style={{position:'absolute',left:60,right:100,top:1420,height:7,background:'#ffffff20'}}><div style={{height:'100%',width:(100*f/239)+'%',background:'#d6f582'}}/></div>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="DirectorSetupTest" component={F} width={1080} height={1920} fps={30} durationInFrames={240}/>);
