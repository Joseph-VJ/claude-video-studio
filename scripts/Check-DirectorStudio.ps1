param([switch]$Mcp)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
Set-Location -LiteralPath 'E:\Video'
$nvencListed=[bool](& ffmpeg -hide_banner -encoders 2>&1 | Select-String 'h264_nvenc')
$checks=[ordered]@{
 date=(Get-Date -Format o)
 root='E:/Video'
 instructionIndex=(Test-Path -LiteralPath 'E:\Video\plans\CLAUDE-FILE-MAP.md')
 directorPlan=(Test-Path -LiteralPath 'E:\Video\plans\CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md')
 renderWorkflow=(Test-Path -LiteralPath 'E:\Video\plans\FAST-RENDER-WORKFLOW-v1.md')
 renderResearch=(Test-Path -LiteralPath 'E:\Video\plans\RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md')
 commands=@(Get-ChildItem -LiteralPath 'E:\Video\.claude\commands' -Filter '*.md' | ForEach-Object {$_.BaseName})
 claude=(& 'C:\Users\Admin\.local\bin\claude.exe' --version | Out-String).Trim()
 node=(& node --version | Out-String).Trim()
 python=(& 'E:\Video\.venv\Scripts\python.exe' --version | Out-String).Trim()
 ffmpeg=(& ffmpeg -version | Select-Object -First 1)
 nvencEncoderListed=$nvencListed
 exporter=(Test-Path -LiteralPath 'E:\Video\scripts\Export-Instagram.ps1')
 timelineColourRenderer=(Test-Path -LiteralPath 'E:\Video\scripts\render-timeline-colour.py')
 defaultColourRoute='render-timeline-colour.py: cut-first, CPU RVM workers + one CuPy colour process + NVENC const-QP a-roll (measured 3.18 fps on the IMG_2442 v12 look)'
 defaultDelivery='Export-Instagram balanced: NVENC p7 tuned CQ24 (~89 MB per 80 s, VMAF 98.4)'
 gpuColourAdapterLegacy=(Test-Path -LiteralPath 'E:\Video\scripts\render-colour-fast.py')
 cupyPackageFilesPresent=(Test-Path -LiteralPath 'E:\Video\tools\cupy-gpu\cupy\__init__.py')
 isolatedOrtGpuFilesPresent=(Test-Path -LiteralPath 'E:\Video\tools\onnx-gpu\onnxruntime\__init__.py')
 defaultMatting='Shared CPU ONNX Runtime / RVM; tested CUDA matting configuration was slower'
 remotionFootageStatus='OffthreadVideo crash and HTML5 frame-timing quality failures remain; no universal browser repair claimed'
 regularChrome=(Test-Path -LiteralPath 'E:\Video\tools\chrome\chrome-win64\chrome.exe')
 compatibleRemotionBinaries=(Test-Path -LiteralPath 'E:\Video\tools\remotion-native-4.0.537\ffprobe.exe')
 free247Commit=(& git -C 'E:\Video\repos\free247editor' rev-parse HEAD | Out-String).Trim()
 herkCommit=(& git -C 'E:\Video\repos\free247editor\kit' rev-parse HEAD | Out-String).Trim()
 sharedLargeModel=(Test-Path -LiteralPath 'E:\Video\models\whisper-large-v3\model.bin')
 sharedMediumModel=(Test-Path -LiteralPath 'E:\Video\models\whisper-medium\model.bin')
 concat=(Test-Path -LiteralPath 'E:\Video\tools\Concat-0.2.8\concat.exe')
 datedRenderEvidence=(Test-Path -LiteralPath 'E:\Video\projects\render-speed-lab-20261025\summary.json')
 verificationScope='Presence/version checks only. Encoder listing is not device execution; use explicit synthetic/sample checks. No creative render or current-file QA performed by this doctor.'
}
if($Mcp){$checks.mcp=(& 'C:\Users\Admin\.local\bin\claude.exe' mcp get concat | Out-String).Trim()}
$destination='E:\Video\logs\studio-doctor'
[IO.Directory]::CreateDirectory($destination) | Out-Null
$json=$checks | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText((Join-Path $destination 'latest.json'),$json,[Text.UTF8Encoding]::new($false))
Write-Output $json
