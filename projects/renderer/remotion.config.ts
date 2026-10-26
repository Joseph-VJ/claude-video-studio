import {Config} from '@remotion/cli/config';
Config.setBrowserExecutable('E:/Video/tools/chrome-headless/chrome-headless-shell-win64/chrome-headless-shell.exe');
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
Config.setConcurrency(2);
Config.setOverwriteOutput(false);
