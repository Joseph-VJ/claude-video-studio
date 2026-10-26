param(
 [Parameter(Mandatory=$true)][string]$EntryFile,
 [Parameter(Mandatory=$true)][string]$Composition,
 [Parameter(Mandatory=$true)][string]$Audio,
 [Parameter(Mandatory=$true)][string]$Output,
 [Parameter(Mandatory=$true)][string]$FramesDirectory,
 [int]$Fps=30,
 [ValidateSet('nvenc','cpu')][string]$Encoder='nvenc',
 [ValidateSet('balanced','max')][string]$Quality='balanced',
 [string]$BrowserExecutable='E:\Video\tools\chrome\chrome-win64\chrome.exe'
)
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
if($Fps -ne 30){throw 'Prepare an explicit 30 fps composition for this Instagram route'}
foreach($target in @($Output,$FramesDirectory)){
 $absoluteTarget=[IO.Path]::GetFullPath($target)
 if(!$absoluteTarget.StartsWith('E:\Video\',[StringComparison]::OrdinalIgnoreCase)){throw 'Render outputs and caches must stay inside E:\Video'}
 if(Test-Path -LiteralPath $absoluteTarget){throw "Choose a fresh path: $absoluteTarget"}
}
foreach($src in @($EntryFile,$Audio)){if(!(Test-Path -LiteralPath $src)){throw "Missing input: $src"}}
[IO.Directory]::CreateDirectory((Split-Path -Parent ([IO.Path]::GetFullPath($Output)))) | Out-Null
$renderLog=[IO.Path]::ChangeExtension($Output,'.render.log')
if(Test-Path -LiteralPath $renderLog){throw 'Choose a new output basename; its render log already exists'}
Push-Location -LiteralPath 'E:\Video\projects\renderer'
try {
 & 'E:\Video\projects\renderer\node_modules\.bin\remotion.cmd' render $EntryFile $Composition $FramesDirectory --sequence --muted --image-format=png --concurrency=2 --binaries-directory='E:\Video\tools\remotion-native-4.0.537' "--browser-executable=$BrowserExecutable" *> $renderLog
 if($LASTEXITCODE -ne 0){throw "Frame render failed; see $renderLog"}
} finally {Pop-Location}
# Preserve the PNGs as the lossless frame cache and encode the upload only once.
& 'E:\Video\scripts\Export-Instagram.ps1' -InputFile $FramesDirectory -OutputFile $Output -AudioFile $Audio -Frames -Encoder $Encoder -Quality $Quality
Write-Output "Rendered PNG frames and exported $Output"
