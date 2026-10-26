$env:TEMP='E:\Video\cache\tmp'
$env:TMP=$env:TEMP
$env:TMPDIR=$env:TEMP
$env:npm_config_cache='E:\Video\cache\npm'
$env:npm_config_prefix='E:\Video\tools\npm'
$env:npm_config_userconfig='E:\Video\tools\npmrc'
$env:npm_config_update_notifier='false'
$env:PIP_CACHE_DIR='E:\Video\cache\pip'
$env:UV_CACHE_DIR='E:\Video\cache\uv'
$env:UV_PYTHON_INSTALL_DIR='E:\Video\tools\python'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPYCACHEPREFIX='E:\Video\cache\python'
$env:HF_HOME='E:\Video\cache\huggingface'
$env:HUGGINGFACE_HUB_CACHE='E:\Video\cache\huggingface\hub'
$env:TORCH_HOME='E:\Video\cache\torch'
$env:XDG_CACHE_HOME='E:\Video\cache\xdg'
$env:XDG_CONFIG_HOME='E:\Video\cache\config'
$env:XDG_DATA_HOME='E:\Video\cache\data'
$env:APPDATA='E:\Video\cache\appdata'
$env:LOCALAPPDATA='E:\Video\cache\localappdata'
$env:PLAYWRIGHT_BROWSERS_PATH='E:\Video\cache\playwright'
$env:PUPPETEER_CACHE_DIR='E:\Video\cache\chrome'
$env:HF_HUB_DISABLE_SYMLINKS_WARNING='1'
$env:HF_HUB_DISABLE_TELEMETRY='1'
$env:DO_NOT_TRACK='1'
$env:Path='E:\Video\.venv\Scripts;E:\Video\projects\renderer\node_modules\.bin;'+$env:Path
$env:CHROME_PATH='E:\Video\tools\chrome\chrome-win64\chrome.exe'
$env:PUPPETEER_EXECUTABLE_PATH=$env:CHROME_PATH
$env:HYPERFRAMES_NO_TELEMETRY='1'
$env:U2NET_HOME='E:\Video\models\u2net'
$env:NUMBA_CACHE_DIR='E:\Video\cache\numba'
$env:NODE_OPTIONS='--require=E:\Video\scripts\node-storage.cjs'
$env:HYPERFRAMES_BROWSER_PATH=$env:CHROME_PATH
$env:HYPERFRAMES_EXTRACT_CACHE_DIR='E:\Video\cache\hyperframes-frames'
$env:HYPERFRAMES_SKIP_SKILLS='1'
$env:SHORT_EDITING_RUNTIME='E:\Video\.agents\skills\short-editing\.runtime'
$env:WHISPER_MODEL='E:\Video\models\whisper-cpp\ggml-large-v3-turbo-q5_0.bin'
$env:HYPERFRAMES_BROWSER_PATH='E:\Video\tools\chrome-headless\chrome-headless-shell-win64\chrome-headless-shell.exe'
$env:VIDEO_WHISPER_MODEL='small'
$env:VIDEO_WHISPER_MODEL_DIR='E:\Video\models\whisper'

$env:PYTHONIOENCODING='utf-8'

$env:CUDA_CACHE_PATH='E:\Video\cache\cuda'

# Project-local Claude storage. Set before invoking Claude.
$env:CLAUDE_CONFIG_DIR='E:\Video\cache\claude'
$env:CLAUDE_CODE_TMPDIR='E:\Video\cache\claude-tmp'
$env:DISABLE_AUTOUPDATER='1'
$env:REMBG_HOME='E:\Video\models\u2netp'
@('E:\Video\cache\tmp','E:\Video\cache\claude-tmp','E:\Video\.context\claude-memory') | ForEach-Object { [IO.Directory]::CreateDirectory($_) | Out-Null }
