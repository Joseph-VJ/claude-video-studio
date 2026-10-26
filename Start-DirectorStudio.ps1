param([switch]$Check,[string]$Project,[Parameter(ValueFromRemainingArguments)][string[]]$ClaudeArgs)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$env:CONCAT_MCP_ROOTS='E:\Video'
Set-Location -LiteralPath 'E:\Video'
if($Project){ & 'E:\Video\.venv\Scripts\python.exe' 'E:\Video\scripts\project-context.py' init --project $Project; if($LASTEXITCODE -ne 0){throw 'Project context initialization failed'} }
if($Check){ & 'E:\Video\scripts\Check-DirectorStudio.ps1'; exit $LASTEXITCODE }
& 'C:\Users\Admin\.local\bin\claude.exe' @ClaudeArgs
