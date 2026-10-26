<#
.SYNOPSIS  Pull the latest studio from GitHub and re-apply your folder paths.
.DESCRIPTION
  The installer rewrites paths inside tracked files. This script undoes that rewrite (so git sees a clean tree), pulls, and runs the installer again
  (finished steps are skipped). It accepts the same options as Install-Studio.ps1, for example:  .\Update-Studio.ps1 -SkipModels
#>
[CmdletBinding()]
param(
    [string]$Python,
    [switch]$Gpu,
    [switch]$SkipModels,
    [switch]$SkipThirdParty,
    [switch]$SkipNode,
    [switch]$SkipPython,
    [switch]$SkipClaudeSettings
)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location -LiteralPath $root
$py = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path (Join-Path $root '.git'))) { throw 'This folder is not a git clone, so it cannot be updated with git pull.' }
if (Test-Path $py) { & $py (Join-Path $root 'scripts\studio-portable.py') revert }
$ErrorActionPreference = 'Continue'   # Windows PowerShell 5.1 treats git's normal progress text on stderr as an error otherwise
& git -C $root pull --ff-only 2>&1 | Out-Host
$pullExit = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($pullExit -ne 0) { throw 'git pull failed. If you edited studio files, commit or stash them first.' }
$forward = @{}
foreach ($k in $PSBoundParameters.Keys) { $forward[$k] = $PSBoundParameters[$k] }
& (Join-Path $root 'Install-Studio.ps1') @forward
