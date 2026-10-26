// Reuse the existing E: Chrome; do not download a second browser or edit D:.
const {createRequire}=require('node:module');
const localRequire=createRequire('D:/gemini-watermark-remover/package.json');
const {chromium}=localRequire('playwright');
const original=chromium.launch.bind(chromium);
chromium.launch=(options={})=>original({...options,executablePath:'E:/Video/tools/chrome-headless/chrome-headless-shell-win64/chrome-headless-shell.exe'});
