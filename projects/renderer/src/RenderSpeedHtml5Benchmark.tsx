import React from 'react';
import {Composition, Html5Video, registerRoot, staticFile} from 'remotion';
const VideoOnly: React.FC = () => <Html5Video src={staticFile('source.mp4')} muted style={{width:1080,height:1920}} />;
const Root: React.FC = () => <Composition id="RenderSpeedHtml5" component={VideoOnly} width={1080} height={1920} fps={30} durationInFrames={270} />;
registerRoot(Root);
