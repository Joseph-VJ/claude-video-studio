import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame,interpolate,spring,staticFile,Sequence} from 'remotion';
import {Video} from '@remotion/media';
import words from './words.json';
const ReelTest:React.FC=()=>{
 const frame=useCurrentFrame();const ms=frame/30*1000;
 const active=words.find(w=>ms>=w.startMs-30&&ms<w.endMs+50);
 const start=active ? active.startMs/1000*30 : 0;
 const scale=active ? spring({frame:Math.max(0,frame-start),fps:30,config:{damping:16,stiffness:230}}) : 1;
 return <AbsoluteFill style={{backgroundColor:'#152638',fontFamily:'Arial, sans-serif'}}>
  <Video src={staticFile('setup-test.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}} />
  <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(8,18,32,.86),rgba(8,18,32,.22) 50%,rgba(8,18,32,.9))'}}/>
  <div style={{position:'absolute',top:280,left:90,right:110,color:'#fff',fontSize:36,fontWeight:700,letterSpacing:5}}>LOCAL VIDEO STUDIO</div>
  <div style={{position:'absolute',top:390,left:90,right:110,color:'#fff',fontSize:82,fontWeight:900,lineHeight:1.05}}>Five seconds.<br/>Every word.<br/><span style={{color:'#e6ff63'}}>Ready to edit.</span></div>
  <div style={{position:'absolute',left:90,right:120,top:1180,height:180,display:'flex',justifyContent:'center',alignItems:'center'}}>
   {active&&<span style={{display:'inline-block',transform:`scale(${.82+.18*scale})`,padding:'22px 42px',borderRadius:22,backgroundColor:'#e6ff63',color:'#102030',fontSize:86,fontWeight:900,boxShadow:'0 12px 35px #0008'}}>{active.text}</span>}
  </div>
  <div style={{position:'absolute',left:90,right:120,top:1405,height:8,background:'#ffffff30',borderRadius:4}}><div style={{width:`${frame/149*100}%`,height:'100%',background:'#e6ff63',borderRadius:4}}/></div>
 </AbsoluteFill>
};
const Root=()=> <Composition id="ReelTest" component={ReelTest} width={1080} height={1920} fps={30} durationInFrames={150}/>;
registerRoot(Root);
