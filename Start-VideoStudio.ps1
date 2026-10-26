param([switch]$ShowTools)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
Set-Location -LiteralPath 'E:\Video'
Write-Host 'Video studio: E:\Video'
Write-Host 'Raw clips: E:\Video\raw | Final videos: E:\Video\out'
if($ShowTools){git --version; node -v; python --version; ffmpeg -version | Select-Object -First 1; yt-dlp --version; hyperframes --help}
