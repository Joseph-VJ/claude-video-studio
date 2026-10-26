param(
 [Parameter(Mandatory)][string]$InputFile,
 [Parameter(Mandatory)][string]$OutputFile,
 [string]$AudioFile,
 [ValidateSet('nvenc','cpu')][string]$Encoder='nvenc',
 [ValidateSet('balanced','max')][string]$Quality='balanced',
 [ValidateSet('master','copy')][string]$AudioMode='master',
 [switch]$Frames,
 [switch]$LosslessArchive
)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$exportArgs=@('E:\Video\scripts\export-instagram.py',$InputFile,$OutputFile,'--encoder',$Encoder,'--quality',$Quality,'--audio-mode',$AudioMode)
if($AudioFile){$exportArgs+=@('--audio',$AudioFile)}
if($Frames){$exportArgs+='--frames'}
if($LosslessArchive){$exportArgs+='--lossless-archive'}
& 'E:\Video\.venv\Scripts\python.exe' @exportArgs
if($LASTEXITCODE -ne 0){throw 'Export failed; inspect its .ffmpeg.log'}
