param([string]$Output,[ValidateSet('nvenc','cpu')][string]$Encoder='nvenc')
$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$stamp=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,6)
if(!$Output){$Output="E:\Video\out\test-render-$stamp.mp4"}
$absoluteOutput=[IO.Path]::GetFullPath($Output)
if(!$absoluteOutput.StartsWith('E:\Video\',[StringComparison]::OrdinalIgnoreCase)){throw 'Output must be inside E:\Video'}
if(Test-Path -LiteralPath $absoluteOutput){throw 'Choose a fresh output'}
$work="E:\Video\work\studio-smoke-$stamp"
[IO.Directory]::CreateDirectory($work) | Out-Null
$master=Join-Path $work 'synthetic-pattern-and-tone.mkv'
& ffmpeg -nostdin -hide_banner -v error -n -f lavfi -i 'testsrc2=size=1080x1920:rate=30:duration=5' -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=5' -c:v ffv1 -level 3 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a pcm_s16le -ac 2 -shortest $master
if($LASTEXITCODE -ne 0){throw 'Synthetic source generation failed'}
& 'E:\Video\scripts\Export-Instagram.ps1' -InputFile $master -OutputFile $absoluteOutput -Encoder $Encoder -Quality balanced
$probeText=(& ffprobe -v error -count_frames -show_streams -show_format -of json $absoluteOutput | Out-String)
if($LASTEXITCODE -ne 0){throw 'Probe failed'}
$probe=$probeText | ConvertFrom-Json
$video=@($probe.streams | Where-Object codec_type -eq 'video')[0]
if($video.width -ne 1080 -or $video.height -ne 1920 -or [int]$video.nb_read_frames -ne 150 -or $video.avg_frame_rate -ne '30/1'){throw 'Synthetic output dimensions/fps/frame count failed'}
& ffmpeg -nostdin -v error -xerror -i $absoluteOutput -f null -
if($LASTEXITCODE -ne 0){throw 'Synthetic full decode failed'}
$receipt=[ordered]@{output=$absoluteOutput;source=$master;frames=150;seconds=5;encoder=$Encoder;fullDecodePassed=$true;scope='Synthetic native encoder test only; browser capture, creative colour, masks and real-video audiovisual QA are not certified'}
$receipt | ConvertTo-Json | Set-Content -LiteralPath ($absoluteOutput+'.smoke.json') -Encoding utf8
$receipt | ConvertTo-Json
