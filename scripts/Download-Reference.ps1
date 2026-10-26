param([Parameter(Mandatory=$true)][string]$Url)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
yt-dlp --ignore-config --no-overwrites --cache-dir 'E:\Video\cache\yt-dlp' --paths 'home:E:\Video\references' --paths 'temp:E:\Video\cache\tmp' --js-runtimes node --merge-output-format mp4 -o '%(extractor)s-%(id)s.%(ext)s' -- $Url
if($LASTEXITCODE -ne 0){throw 'Reference download failed; preserve any partial files and inspect the error'}
