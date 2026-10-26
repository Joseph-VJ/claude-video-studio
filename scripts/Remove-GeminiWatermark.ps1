param([Parameter(Mandatory)][string]$InputFile,[Parameter(Mandatory)][string]$OutputFile)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$inputPath=(Resolve-Path -LiteralPath $InputFile).Path
$outputPath=[IO.Path]::GetFullPath($OutputFile)
if(-not $outputPath.StartsWith('E:\Video\',[StringComparison]::OrdinalIgnoreCase)){throw 'Save processed assets inside E:\Video'}
if(Test-Path -LiteralPath $outputPath){throw 'Choose a fresh output filename'}
New-Item -ItemType Directory -Path (Split-Path $outputPath) -Force | Out-Null
$oldOptions=$env:NODE_OPTIONS
try {
    $env:NODE_OPTIONS += ' --require=E:\Video\scripts\gemini-browser.cjs'
    $result=& node 'D:\gemini-watermark-remover\bin\gwr.mjs' remove $inputPath --output $outputPath --json --video-timeout-ms 180000
    $result | Set-Content -LiteralPath ($outputPath+'.gwr.json') -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Gemini watermark processing failed; inspect output .gwr.json'}
    Write-Output "Processed asset: $outputPath"
    Write-Output "Visual review required; inspect the output, not only its clean metadata."
} finally { $env:NODE_OPTIONS=$oldOptions }
