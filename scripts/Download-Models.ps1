param([string]$Root = (Split-Path -Parent $PSScriptRoot))
# Downloads the small ONNX models the studio needs and verifies each SHA-256. Safe to re-run.
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'models.json') -Raw | ConvertFrom-Json
$failed = 0
function Get-Sha256($path) {   # built-in .NET hashing: does not depend on the Get-FileHash cmdlet being available
    $sha = [Security.Cryptography.SHA256]::Create(); $fs = [IO.File]::OpenRead($path)
    try { return ([BitConverter]::ToString($sha.ComputeHash($fs)) -replace '-', '').ToLower() } finally { $fs.Dispose(); $sha.Dispose() }
}
foreach ($m in $manifest.models) {
    $dest = Join-Path $Root ($m.path -replace '/', '\')
    if ((Test-Path -LiteralPath $dest) -and ((Get-Sha256 $dest) -eq $m.sha256)) {
        Write-Host ("[ok]   {0} already present and verified" -f $m.name); continue
    }
    [IO.Directory]::CreateDirectory((Split-Path -Parent $dest)) | Out-Null
    $tmp = "$dest.part"
    Write-Host ("[get]  {0} ({1:N1} MB) {2}" -f $m.name, ($m.bytes / 1MB), $m.license)
    try {
        Invoke-WebRequest -Uri $m.url -OutFile $tmp -UseBasicParsing
        $hash = Get-Sha256 $tmp
        if ($hash -ne $m.sha256) { Remove-Item -LiteralPath $tmp -Force; throw ("hash mismatch for {0}: expected {1}, got {2}" -f $m.name, $m.sha256, $hash) }
        Move-Item -LiteralPath $tmp -Destination $dest -Force
        Write-Host ("[ok]   {0} verified" -f $m.name)
    } catch {
        $failed++; Write-Warning ("{0} failed: {1}" -f $m.name, $_.Exception.Message)
    }
}
Write-Host $manifest.whisper
if ($failed -gt 0) { exit 1 }
