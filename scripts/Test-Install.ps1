param([string]$Root = (Split-Path -Parent $PSScriptRoot))
# Quick, honest checks that the studio is installed. Presence checks plus a few real imports/calls; it does not render a video.
$ErrorActionPreference = 'Continue'
$rows = New-Object System.Collections.ArrayList
function Add-Row($name, $ok, $detail, $required = $true) { [void]$rows.Add([pscustomobject]@{Check = $name; Result = $(if ($ok) { 'ok' } elseif ($required) { 'FAIL' } else { 'skip' }); Detail = $detail; Required = $required }) }
$py = Join-Path $Root '.venv\Scripts\python.exe'

Add-Row 'studio instructions' ((Test-Path "$Root\CLAUDE.md") -and (Test-Path "$Root\plans\CLAUDE-FILE-MAP.md")) 'CLAUDE.md + plans'
Add-Row 'commands and skills' ((Test-Path "$Root\.claude\commands\video-director.md") -and (Test-Path "$Root\.claude\skills\video-design\SKILL.md")) '.claude\commands, .claude\skills'
$pyOk = Test-Path -LiteralPath $py
Add-Row 'python venv' $pyOk $(if ($pyOk) { (& $py --version 2>&1) } else { 'missing .venv' })
if ($pyOk) {
    $code = "import numpy, PIL, av, onnxruntime, faster_whisper, yaml; print('numpy', numpy.__version__, 'onnxruntime', onnxruntime.__version__, 'av', av.__version__)"
    $o = & $py -c $code 2>&1
    Add-Row 'python packages import' ($LASTEXITCODE -eq 0) (($o | Out-String).Trim().Split("`n")[-1])
    $o = & $py -I "$Root\scripts\project-context.py" disk 2>&1
    Add-Row 'project-context.py runs' ($LASTEXITCODE -eq 0) (($o | Out-String).Trim().Substring(0, [Math]::Min(60, ($o | Out-String).Trim().Length)))
    $o = & $py -m py_compile "$Root\scripts\export-instagram.py" "$Root\scripts\render-timeline-colour.py" "$Root\.claude\skills\video-design\scripts\design-audit.py" 2>&1
    Add-Row 'studio scripts compile' ($LASTEXITCODE -eq 0) 'export, timeline renderer, design audit'
}
$ffOk = (Get-Command ffmpeg -ErrorAction SilentlyContinue) -and (Get-Command ffprobe -ErrorAction SilentlyContinue)
Add-Row 'ffmpeg + ffprobe' $ffOk $(if ($ffOk) { (& ffmpeg -version 2>&1 | Select-Object -First 1) } else { 'not on PATH' })
if ($ffOk) {
    $enc = (& ffmpeg -hide_banner -encoders 2>&1 | Out-String)
    Add-Row 'libx264 encoder' ($enc -match 'libx264') 'CPU H.264 export (always works)'
    Add-Row 'h264_nvenc encoder listed' ($enc -match 'h264_nvenc') 'listed only; a real NVIDIA GPU is needed to use it' $false
}
Add-Row 'node 20+' ((Get-Command node -ErrorAction SilentlyContinue) -and ([int](& node --version).TrimStart('v').Split('.')[0] -ge 20)) $(if (Get-Command node -ErrorAction SilentlyContinue) { & node --version } else { 'missing' })
Add-Row 'Remotion installed' (Test-Path "$Root\projects\renderer\node_modules\.bin\remotion.cmd") 'projects\renderer' $false
$chrome = $null; foreach ($p in @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe")) { if ($p -and (Test-Path -LiteralPath $p)) { $chrome = $p; break } }
Add-Row 'Google Chrome (for graphics)' ([bool]$chrome) $(if ($chrome) { $chrome } else { 'not found' })
Add-Row 'claude CLI' ([bool](Get-Command claude -ErrorAction SilentlyContinue)) $(if (Get-Command claude -ErrorAction SilentlyContinue) { (& claude --version 2>&1 | Select-Object -First 1) } else { 'not installed' })
$manifest = Get-Content -LiteralPath "$Root\scripts\models.json" -Raw | ConvertFrom-Json
foreach ($m in $manifest.models) {
    $f = Join-Path $Root ($m.path -replace '/', '\')
    $good = $false
    if (Test-Path -LiteralPath $f) { $sha = [Security.Cryptography.SHA256]::Create(); $fs = [IO.File]::OpenRead($f); try { $good = (([BitConverter]::ToString($sha.ComputeHash($fs)) -replace '-', '').ToLower() -eq $m.sha256) } finally { $fs.Dispose(); $sha.Dispose() } }
    Add-Row ("model " + $m.name) $good $(if ($good) { 'hash verified' } else { 'missing: run scripts\Download-Models.ps1' }) $false
}
foreach ($s in 'short-editing', 'video-edit', 'hyperframes', 'vox') { Add-Row ("upstream skill " + $s) (Test-Path "$Root\.agents\skills\$s\SKILL.md") '.agents\skills' $false }
Add-Row 'free247editor / Herk kit' (Test-Path "$Root\repos\free247editor\kit") 'repos\free247editor' $false
Add-Row 'paths point at this folder' (($Root -ieq 'E:\Video') -or (Test-Path -LiteralPath "$Root\.studio-portable.json")) 'studio-portable.py apply has run'

$rows | Format-Table Check, Result, Detail -AutoSize -Wrap | Out-String -Width 200 | Write-Host
$fail = @($rows | Where-Object { $_.Result -eq 'FAIL' }).Count
if ($fail) { Write-Host "$fail required check(s) failed." -ForegroundColor Red; exit 1 } else { Write-Host 'All required checks passed.' -ForegroundColor Green; exit 0 }
