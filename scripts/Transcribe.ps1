param([Parameter(Mandatory=$true)][string]$Video,[string]$Output,[string]$Language,[string]$Prompt)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$transcribeArgs=@('E:\Video\scripts\transcribe.py',$Video)
if($Output){$transcribeArgs+=@('--output',$Output)}
if($Language){$transcribeArgs+=@('--language',$Language)}
if($Prompt){$transcribeArgs+=@('--prompt',$Prompt)}
& 'E:\Video\.venv\Scripts\python.exe' @transcribeArgs
if($LASTEXITCODE -ne 0){throw 'Transcription failed'}
