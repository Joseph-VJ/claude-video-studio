const os=require('node:os');
const fs=require('node:fs');
const root='E:/Video/cache/user';
fs.mkdirSync(root,{recursive:true});
os.homedir=()=>root;
os.tmpdir=()=>'E:/Video/cache/tmp';
require('node:module').syncBuiltinESMExports();
