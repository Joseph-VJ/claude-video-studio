param([switch]$Check,[Parameter(ValueFromRemainingArguments)][string[]]$ClaudeArgs)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
Set-Location -LiteralPath 'E:\Video'
$claudeExe='C:\Users\Admin\.local\bin\claude.exe'
if(!(Test-Path -LiteralPath $claudeExe)){throw 'Claude Code executable not found'}
if($Check){ & $claudeExe --version;exit $LASTEXITCODE }
& $claudeExe @ClaudeArgs
