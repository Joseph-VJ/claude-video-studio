<#
.SYNOPSIS
  One-command setup of the Claude Video Studio on Windows 10/11.

.DESCRIPTION
  Run this from the folder you cloned the repo into. It checks the tools you need, optionally installs missing ones with winget,
  creates a Python environment, fetches the third-party editing kits (from their own upstream, at pinned versions), installs the Remotion
  graphics project, downloads the small ONNX models (hash-checked), points every path in the studio at THIS folder, and wires Claude's
  hooks and status line. It is safe to run again: finished steps are skipped.

.EXAMPLE
  git clone https://github.com/Joseph-VJ/claude-video-studio.git C:\VideoStudio
  cd C:\VideoStudio
  .\Install-Studio.ps1 -InstallPrerequisites

.PARAMETER Python                Full path to a Python 3.12 python.exe, if the installer cannot find one (for example a stale `py` launcher).
.PARAMETER InstallPrerequisites  Install missing git / Node LTS / Python 3.12 / FFmpeg / Chrome / PowerShell 7 with winget.
.PARAMETER Gpu                   NVIDIA extras: CUDA libraries for faster-whisper and CuPy for GPU colour (optional, large).
.PARAMETER SkipModels            Do not download the ONNX models.
.PARAMETER SkipThirdParty        Do not fetch the upstream editing kits.
.PARAMETER SkipNode              Do not install the Remotion graphics project.
.PARAMETER SkipPython            Do not create the Python environment.
.PARAMETER SkipClaudeSettings    Do not write Claude hooks / status line into cache\claude\settings.json.
.PARAMETER CheckOnly             Only report what is installed.
#>
[CmdletBinding()]
param(
    [string]$Root = $PSScriptRoot,
    [string]$Python,
    [switch]$InstallPrerequisites,
    [switch]$Gpu,
    [switch]$SkipModels,
    [switch]$SkipThirdParty,
    [switch]$SkipNode,
    [switch]$SkipPython,
    [switch]$SkipClaudeSettings,
    [switch]$CheckOnly
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$Root = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\')
if ($Root -ne $PSScriptRoot.TrimEnd('\')) { throw "Run the installer that lives inside the studio folder you want to set up (this one is in $PSScriptRoot, but -Root is $Root)." }
Set-Location -LiteralPath $Root   # every relative path below is relative to the studio folder, never to wherever the shell happened to be
$script:problems = New-Object System.Collections.ArrayList

function Step($t) { Write-Host ""; Write-Host "== $t" -ForegroundColor Cyan }
function Ok($t)   { Write-Host "  [ok]   $t" -ForegroundColor Green }
function Warn($t) { Write-Host "  [warn] $t" -ForegroundColor Yellow }
function Need($t) { Write-Host "  [need] $t" -ForegroundColor Red; [void]$script:problems.Add($t) }
function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Refresh-Path { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }
function Run($exe, $arguments, $dir) {
    $p = Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory $dir -NoNewWindow -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw ("{0} {1} failed with exit code {2}" -f $exe, ($arguments -join ' '), $p.ExitCode) }
}

function Find-Python {
    if ($Python) { if (Test-Path -LiteralPath $Python) { return (Resolve-Path -LiteralPath $Python).Path } else { return $null } }
    foreach ($try in @(@('py', '-3.12'), @('python'), @('python3'))) {
        $exe = $try[0]
        if (-not (Have $exe)) { continue }
        $extra = @(); if ($try.Length -gt 1) { $extra = $try[1..($try.Length - 1)] }
        try {
            $o = & $exe @extra -c 'import sys;print(sys.version_info[0],sys.version_info[1]);print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0 -and $o[0] -eq '3 12') { return $o[1] }
        } catch { }
    }
    return $null
}
function Find-Chrome {
    foreach ($p in @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe")) {
        if ($p -and (Test-Path -LiteralPath $p)) { return $p }
    }
    return $null
}
function Node-Ok { if (-not (Have node)) { return $false }; try { return ([int](& node --version).TrimStart('v').Split('.')[0] -ge 20) } catch { return $false } }

Write-Host "Claude Video Studio installer" -ForegroundColor White
Write-Host "Studio folder: $Root"
if ($Root -match '\s') { Warn "The folder path contains spaces. It works, but a short path such as C:\VideoStudio is safer." }

# ---------------------------------------------------------------------------------------------------------------- 1. prerequisites
Step '1/9  Checking tools'
$wanted = @(
    @{Name = 'git';              Test = { Have git };                       Id = 'Git.Git' },
    @{Name = 'Node.js 20+';      Test = { Node-Ok };                        Id = 'OpenJS.NodeJS.LTS' },
    @{Name = 'Python 3.12';      Test = { [bool](Find-Python) };            Id = 'Python.Python.3.12' },
    @{Name = 'FFmpeg + ffprobe'; Test = { (Have ffmpeg) -and (Have ffprobe) }; Id = 'Gyan.FFmpeg' },
    @{Name = 'Google Chrome';    Test = { [bool](Find-Chrome) };            Id = 'Google.Chrome' },
    @{Name = 'PowerShell 7 (optional)'; Test = { Have pwsh };              Id = 'Microsoft.PowerShell'; Optional = $true }
)
foreach ($w in $wanted) {
    if (& $w.Test) { Ok $w.Name; continue }
    if ($InstallPrerequisites -and -not $CheckOnly) {
        if (-not (Have winget)) { Need "$($w.Name) is missing and winget is not available. Install it manually."; continue }
        Write-Host "  installing $($w.Name) with winget ($($w.Id)) ..."
        & winget install --exact --id $w.Id --silent --accept-package-agreements --accept-source-agreements | Out-Null
        Refresh-Path
        if (& $w.Test) { Ok "$($w.Name) installed" } elseif (-not $w.Optional) { Need "$($w.Name) was installed but is not visible yet. Open a NEW PowerShell window and run this installer again." }
    } elseif ($w.Optional) { Warn "$($w.Name) not found (the .cmd launcher falls back to Windows PowerShell)" }
    else { Need "$($w.Name) is missing. Install it with:  winget install --exact --id $($w.Id)   (or re-run with -InstallPrerequisites)" }
}
if (Have claude) { Ok 'Claude Code (claude)' } else { Need 'Claude Code is not installed. Install it with:  irm https://claude.ai/install.ps1 | iex   (then sign in by running: claude)' }
if (Have nvidia-smi) { Ok 'NVIDIA GPU found (optional GPU colour and NVENC export can be used)' } else { Warn 'No NVIDIA GPU detected: the studio uses its CPU paths (slower, fully supported for editing and export)' }
if ($CheckOnly) { if ($script:problems.Count) { exit 1 } else { Write-Host "`nEverything required is present." -ForegroundColor Green; exit 0 } }
if ($script:problems.Count) { Write-Host "`nFix the items marked [need], then run this installer again." -ForegroundColor Red; exit 1 }

# ---------------------------------------------------------------------------------------------------------------- 2. folders
Step '2/9  Creating folders'
foreach ($d in 'raw', 'out', 'work', 'logs', 'models', 'assets', 'projects', 'repos', 'tools\npm', '.context\claude-memory', 'cache\tmp', 'cache\claude', 'cache\claude-tmp', 'cache\npm', 'cache\pip', 'cache\huggingface') {
    [IO.Directory]::CreateDirectory((Join-Path $Root $d)) | Out-Null
}
if (-not (Test-Path (Join-Path $Root 'tools\npmrc'))) { Set-Content -LiteralPath (Join-Path $Root 'tools\npmrc') -Value '' -Encoding ASCII }
Ok 'raw\ (put your recordings here), out\ (finished videos), work\, models\, projects\'

# ---------------------------------------------------------------------------------------------------------------- 3. python
$venvPy = Join-Path $Root '.venv\Scripts\python.exe'
Step '3/9  Python environment'
if ($SkipPython) { Warn 'skipped' } else {
    if (-not (Test-Path -LiteralPath $venvPy)) { Write-Host '  creating .venv ...'; & (Find-Python) -m venv (Join-Path $Root '.venv'); if ($LASTEXITCODE -ne 0) { throw 'could not create the virtual environment' } }
    $env:PIP_CACHE_DIR = Join-Path $Root 'cache\pip'
    & $venvPy -m pip install --quiet --upgrade pip
    $lock = Get-Content -LiteralPath (Join-Path $Root 'requirements.lock.txt')
    $core = $lock | Where-Object { $_ -notmatch '^\s*nvidia-' -and $_.Trim() -ne '' }
    $req = Join-Path $Root 'cache\requirements-core.txt'
    Set-Content -LiteralPath $req -Value $(if ($Gpu) { $lock } else { $core }) -Encoding ASCII
    Write-Host "  installing $(@(Get-Content $req).Count) pinned packages (first run downloads a few hundred MB) ..."
    & $venvPy -m pip install --quiet -r $req
    if ($LASTEXITCODE -ne 0) { throw 'pip install failed (see the message above)' }
    Ok "Python packages installed ($(& $venvPy --version))"
    if ($Gpu) {
        $cupy = Join-Path $Root 'tools\cupy-gpu'
        Write-Host '  installing CuPy (GPU colour) into tools\cupy-gpu ...'
        & $venvPy -m pip install --quiet --target $cupy 'cupy-cuda12x==14.2.0'
        if ($LASTEXITCODE -eq 0) { Ok 'CuPy installed' } else { Warn 'CuPy install failed; GPU colour stays unavailable, CPU colour still works' }
    }
}

# ---------------------------------------------------------------------------------------------------------------- 4. portable paths
Step '4/9  Pointing the studio at this folder'
$chrome = Find-Chrome
$portArgs = @((Join-Path $Root 'scripts\studio-portable.py'), 'apply', '--root', $Root)
if ($chrome) { $portArgs += @('--chrome', $chrome) }
if (Test-Path -LiteralPath $venvPy) { & $venvPy @portArgs } else { & (Find-Python) @portArgs }
if ($LASTEXITCODE -ne 0) { throw 'path rewrite failed' }
Ok "all studio files now use $Root"

# ---------------------------------------------------------------------------------------------------------------- 5. third-party
Step '5/9  Editing kits from their upstream projects'
function Clone-Pinned($url, $commit, $dest) {
    if (Test-Path -LiteralPath (Join-Path $dest '.git')) { Ok "$(Split-Path $dest -Leaf) already present"; return }
    if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
    [IO.Directory]::CreateDirectory($dest) | Out-Null
    & git -C $dest init --quiet
    & git -C $dest remote add origin $url
    & git -C $dest fetch --quiet --depth 1 origin $commit
    if ($LASTEXITCODE -ne 0) { throw "could not fetch $url at $commit" }
    & git -C $dest -c advice.detachedHead=false checkout --quiet FETCH_HEAD
}
if ($SkipThirdParty) { Warn 'skipped' } else {
    $tp = Get-Content -LiteralPath (Join-Path $Root 'scripts\third-party.json') -Raw | ConvertFrom-Json
    $skills = Join-Path $Root '.agents\skills'
    [IO.Directory]::CreateDirectory($skills) | Out-Null
    $tmpRoot = Join-Path $Root 'cache\third-party'
    foreach ($s in $tp.skillSources) {
        $tmp = Join-Path $tmpRoot $s.name
        if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
        Write-Host "  fetching $($s.name) ($($s.license)) ..."
        Clone-Pinned $s.url $s.commit $tmp
        if ($s.copyDirsFrom) {
            Get-ChildItem -LiteralPath (Join-Path $tmp ($s.copyDirsFrom)) -Directory | ForEach-Object {
                $target = Join-Path $skills $_.Name
                if (-not (Test-Path -LiteralPath $target)) { Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse }
            }
        }
        if ($s.copyWholeRepoTo) {
            $target = Join-Path $Root ($s.copyWholeRepoTo -replace '/', '\')
            if (-not (Test-Path -LiteralPath $target)) { [IO.Directory]::CreateDirectory($target) | Out-Null; Get-ChildItem -LiteralPath $tmp -Force | Where-Object Name -ne '.git' | Copy-Item -Destination $target -Recurse }
        }
        Ok "$($s.name) @ $($s.commit.Substring(0, 10))"
    }
    $hf = Join-Path $Root 'third_party\hyperframes-skills'
    if (Test-Path -LiteralPath $hf) {
        Get-ChildItem -LiteralPath $hf -Directory | ForEach-Object { $t = Join-Path $skills $_.Name; if (-not (Test-Path -LiteralPath $t)) { Copy-Item -LiteralPath $_.FullName -Destination $t -Recurse } }
        Ok 'HyperFrames skills (Apache-2.0, bundled)'
    }
    foreach ($r in $tp.repos) {
        $dest = Join-Path $Root ($r.into -replace '/', '\')
        Clone-Pinned $r.url $r.commit $dest
        if ((Test-Path (Join-Path $dest 'setup.mjs')) -and -not (Test-Path (Join-Path $dest 'kit\.git'))) {
            Write-Host "  running $($r.name) setup (installs the Herk Edit Kit) ..."
            try { Run 'node' @('setup.mjs') $dest } catch { Warn "$($r.name) setup did not finish: $($_.Exception.Message). Run 'node setup.mjs' inside repos\free247editor later; the other routes keep working." }
        }
        Ok "$($r.name) @ $($r.commit.Substring(0, 10))"
    }
}

# ---------------------------------------------------------------------------------------------------------------- 6. node
Step '6/9  Remotion graphics project'
$rend = Join-Path $Root 'projects\renderer'
if ($SkipNode) { Warn 'skipped' } elseif (Test-Path -LiteralPath (Join-Path $rend 'package.json')) {
    if (Test-Path -LiteralPath (Join-Path $rend 'node_modules\.bin\remotion.cmd')) { Ok 'already installed' } else {
        Write-Host '  npm ci (downloads Remotion, about 300 MB) ...'
        $env:npm_config_update_notifier = 'false'
        Run 'npm.cmd' @('ci', '--no-audit', '--no-fund') $rend
        Ok 'Remotion installed'
    }
    $native = Join-Path $Root 'tools\remotion-native-4.0.537'
    [IO.Directory]::CreateDirectory($native) | Out-Null
    $ff = Split-Path -Parent (Get-Command ffmpeg).Source
    foreach ($f in 'ffmpeg.exe', 'ffprobe.exe') { if (Test-Path (Join-Path $ff $f)) { Copy-Item (Join-Path $ff $f) $native -Force } }
    Get-ChildItem -LiteralPath $ff -Filter '*.dll' -ErrorAction SilentlyContinue | Copy-Item -Destination $native -Force
    Ok 'Remotion helper binaries (system FFmpeg/ffprobe) prepared'
} else { Warn 'projects\renderer\package.json not found' }

# ---------------------------------------------------------------------------------------------------------------- 7. models
Step '7/9  Models (hash-checked)'
if ($SkipModels) { Warn 'skipped (run scripts\Download-Models.ps1 later)' } else {
    try { & (Join-Path $Root 'scripts\Download-Models.ps1') -Root $Root } catch { Warn "model download failed: $($_.Exception.Message). Run scripts\Download-Models.ps1 again later." }
}

# ---------------------------------------------------------------------------------------------------------------- 8. claude settings
Step '8/9  Claude hooks and status line'
if ($SkipClaudeSettings) { Warn 'skipped' } else {
    $tmplPath = Join-Path $Root 'config\claude-settings.template.json'
    $dest = Join-Path $Root 'cache\claude\settings.json'
    $tmpl = Get-Content -LiteralPath $tmplPath -Raw | ConvertFrom-Json
    if (Test-Path -LiteralPath $dest) { $cur = Get-Content -LiteralPath $dest -Raw | ConvertFrom-Json } else { $cur = [pscustomobject]@{} }
    foreach ($k in 'autoMemoryDirectory', 'statusLine', 'hooks') { $cur | Add-Member -NotePropertyName $k -NotePropertyValue $tmpl.$k -Force }
    [IO.File]::WriteAllText($dest, ($cur | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
    Ok "settings written to cache\claude\settings.json (your sign-in is stored there by Claude itself and is never committed)"
}

# ---------------------------------------------------------------------------------------------------------------- 9. self test
Step '9/9  Self test'
& (Join-Path $Root 'scripts\Test-Install.ps1') -Root $Root
Write-Host ""
Write-Host "Done. Start the studio:" -ForegroundColor Green
Write-Host "  $Root\Start-DirectorStudio.cmd"
Write-Host "Then in Claude, for example:"
Write-Host '  /video-director Edit raw\my-video.mp4 into a clear Instagram Reel. Inspect it first, make a plan, then a versioned draft.'
Write-Host "First time only: Claude asks you to sign in inside that window. Your recordings stay on this PC (put them in raw\)."
