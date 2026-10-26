import React from 'react';
import {Composition, OffthreadVideo, registerRoot, staticFile} from 'remotion';
const VideoOnly: React.FC = () => <OffthreadVideo src={staticFile('source.mkv')} muted style={{width:1080,height:1920}} />;
const Root: React.FC = () => <Composition id="RenderSpeedVideo" component={VideoOnly} width={1080} height={1920} fps={30} durationInFrames={270} />;
registerRoot(Root);
