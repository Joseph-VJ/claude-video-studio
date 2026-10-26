# Fast render workflow for Claude — v1

Updated 2026-10-25 (defaults revised the same evening: cut-first timeline renderer + `balanced` delivery, see plans/TIMELINE-RENDERER-v1.md). Applies to E:/Video on this Ryzen 5 3500 / GTX 1650 4 GB / 32 GB PC. Read the current brief first. Use `/video-render-fast` for this workflow. Evidence is in `projects/render-speed-lab-20261025`; that folder must never become the default new-video project.

Read only the relevant stage: [1: Start with this video's content and settings](#1-start-with-this-videos-content-and-settings) | [2: Measure the bottleneck](#2-measure-the-bottleneck) | [3: Choose the least costly suitable route](#3-choose-the-least-costly-suitable-route) | [4: Custom GPU colour adapter](#4-custom-gpu-colour-adapter) | [5: Cache and revise efficiently](#5-cache-and-revise-efficiently) | [6: Export the upload once](#6-export-the-upload-once) | [7: Remotion and Concat limits](#7-remotion-and-concat-limits) | [8: Verify the exact output](#8-verify-the-exact-output) | [9: Revision invalidation and the render handoff](#9-revision-invalidation-and-the-render-handoff) | [10: Exact local command recipes](#10-exact-local-command-recipes) | [11: Installed tool map and when to use each](#11-installed-tool-map-and-when-to-use-each) | [12: Readiness and evidence](#12-readiness-and-evidence)

## 1. Start with this video's content and settings

For each NEW video inspect actual footage, dialogue/transcript, motion, exposure, lighting, orientation, fps and HDR metadata. Write a fresh audience/story/edit plan with source anchors before selecting a treatment. Do not reuse the last video's grade, white balance, face boxes, background masks, graphics, colour correction or cut decisions. Existing long-term preferences may guide questions; they do not supply a ready-made grade. An export of an already approved edit retains that edit's settings.

List the work before executing it. Keep original media and existing approved versions. Load `scripts/env.ps1`; use `E:/Video/.venv/Scripts/python.exe`. Keep new tools, caches and outputs on E:. Reuse installed software before installing another repository. Never upload footage or publish by implication.

## 2. Measure the bottleneck

Record separate timings for decode/HDR conversion, matting, colour, graphics and delivery encoding. Test representative details, movement, gradients, dark and bright shots, and graphics transitions. Do not use CPU percentage, RAM occupancy or a CUDA provider name as evidence of acceleration. GPU Video Encode and CUDA/3D are different engines. High RAM use is not a performance target.

The tests here found expensive NumPy colour math, software x264 finishing and a Windows unbuffered-pipe allocation issue. `render-colour-fast.py` fixes the pipe issue by allocating one buffer and calling `readinto`; it does not alter pixel data to get that benefit. NVDEC was tested but did not improve the small decode-only sample, so it is not forced on.

## 3. Choose the least costly suitable route

| Work | Route | Conditions |
|---|---|---|
| Remux or join compatible unchanged streams | FFmpeg stream copy / concat demuxer | Matching codecs/parameters/timebases; review keyframe boundaries, timestamps and audio sync. Exact arbitrary cuts, effects and transitions may require encoding. |
| Scale, crop, basic colour, audio and final encode | Existing FFmpeg | Keep one deliberate colour interpretation and one delivery video encode. |
| Native timeline transforms/effects/text | Concat 0.2.8 MCP | GPU DX12 compositor is verified. Validate the actual input format and frame cadence. Its H.264 path prefers libx264; drawing on the GPU is not NVENC encoding. |
| Specific React/GSAP graphics | Remotion, only where needed | Use current assets and installed Chrome. Avoid sending unneeded plain footage through browser PNG capture. Do not automatically rewrite existing compositions. |
| **Default:** current-job colour module over the edit | `scripts/render-timeline-colour.py config.json` | Cut-first: grades only the edit's segments; CPU RVM worker processes + ONE CuPy colour process + direct NVENC const-QP a-roll (+ optional FFV1 archive) + audio cut/mux. Measured 3.18 fps vs ~0.97 fps for the chunk+join+recut route. Requires current-job module/parameters and a short parity sample. |
| Legacy full-length colour cache / numerical CPU-GPU parity reference | `scripts/render-colour-fast.py job.json` | Grades every source frame into a 16-bit FFV1 cache; for parity checks only, not normal edits (its join + recut cost ~18 min on an 80 s Reel). |
| Final Instagram MP4 from SDR master / PNG frames | `scripts/Export-Instagram.ps1` | `balanced` by default (NVENC p7 tuned CQ24, ~89 MB per 80 s); `max` (tuned CQ20) only on request; CPU fallback selected explicitly and recorded. |

Do not render an entire raw recording when only planned ranges plus transition/matte handles are used. Keep temporal matting sequential and carry its recurrent state. For separate chunks include explicit warm-up frames; never reset state every frame or lower the matte resolution just to show a speed gain. Record the exact range and warm-up in the cache identity.

A native compositor cannot reproduce an arbitrary Python colour function automatically. A project with an approved look needs a verified conversion, not an approximate filter substituted for speed.

## 4. Custom GPU colour adapter

The same module interface is used by the default cut-first renderer (`scripts/render-timeline-colour.py`, section 10) and by this full-length adapter, which is now the parity/reference tool. This is a validated adapter for a specific function interface, not a universal colour plugin. The reviewed job module must expose `R`, `MASK`, `luma`, `smoothstep`, `box_blur` and `correct(base, face, parameters, shirt_gains, alpha=...)`. Its helpers must be compatible with CuPy. Its geometry is explicitly 1080x1920; its only reviewed preprocessing route is HLG BT.2020 -> linear -> Hable -> Rec.709. Other inputs fail instead of receiving an invented conversion.

The JSON must explicitly supply `input`, `output` (fresh .mkv), `grade_module`, every parameter in the module's `R`, `shirt_gains`, `width`, `height`, `preprocess`, `start`, `frames`, `compute`, `dither_strength`, `dither_seed` and `matte_warmup_frames`. Add `module_sha256` to reject a changed colour module. Choose the new video's actual masks and measured settings. Do not copy the lab's job JSON: it deliberately contains the old v11 look for benchmarking.

Use `compute: gpu` for the tested CuPy path, or `cpu` for a numerical reference. The adapter keeps CPU RVM inference because the tested isolated CUDA version was slower on this card. It retains recurrent state. Dither is explicit: zero in parity tests; an approved strength/seed in a real job. The old renderer used random dither of 1/255, so a no-dither test is not an exact reproduction of the historical final output.

The 16-bit RGB FFV1 cache preserves the adapter's computed and quantised frames. It does not restore detail already lost in original compression. Check disk capacity: full-resolution lossless caches can be large. The manifest records source SHA256, explicit configuration, module/helper hashes, model, Python/NumPy/CuPy/FFmpeg identities and a cache key. There is no automatic reuse of old project output. Changed dependencies/source metadata fail promotion. Validate a few seconds with the current shot, including matte edges, before full production.

## 5. Cache and revise efficiently

Use a current-project `work/` directory. Cache transcription, source mapping, matte/graded frames and motion sections independently. Reuse a stage only when its source hash, source ranges, relevant settings, masks/geometry, colour space, model/runtime and temporal state match. Changing captions should not re-run the grade; changing audio should not re-render picture. New footage gets new analysis and creative settings even if the camera or speaker is the same.

Keep diagnostic logs and compact JSON manifests; read the necessary ranges instead of pasting long logs into Claude context. Save the job state in the project's `.context/STATE.md`. Never point the active project to a benchmark folder by accident. Do not delete a source or approved master while clearing a cache.

## 6. Export the upload once

The default MP4 preset `balanced` is H.264 NVENC p7/hq, VBR CQ24, spatial AQ 8, temporal AQ, 32-frame lookahead, full-resolution multipass, B-frames as middle references (3 B-frames), 24 Mb/s rate-control ceiling, 48 Mb buffer, 1080x1920 30 fps, 8-bit 4:2:0, Rec.709 limited range, GOP60 and faststart. Measured on the IMG_2442 v12 master: 84.8 MB for the 79.6 s export (old CQ20 default: 137.6 MB), VMAF 98.4 / 47.7 dB on a 15 s excerpt, and no visible difference in zoomed face, text-edge and fabric crops. `max` (tuned CQ20) gives ~151 MB per 80 s, VMAF 98.9. Actual bitrate varies with content. The 24 Mb/s setting is not a file-size guarantee or a promise that Instagram will not recompress it. A new source with fine noise/fast movement must get a fresh quality check.

```powershell
. 'E:\Video\scripts\env.ps1'
& 'E:\Video\scripts\Export-Instagram.ps1' `
  -InputFile 'E:\Video\projects\CURRENT\work\approved-sdr-master.mov' `
  -AudioFile 'E:\Video\projects\CURRENT\work\approved-premix.wav' `
  -OutputFile 'E:\Video\out\CURRENT-instagram-v1.mp4'
```

For existing contiguous `element-NNN.png` frames, use `-InputFile <frames-directory> -Frames -AudioFile <mix>`. This directly encodes one MP4 and retains the PNG cache. `Render-DirectorProject.ps1` now uses this path after frame capture, without an intermediate H.264 generation. The previous helper is saved as `Render-DirectorProject.pre-fast-render-20261025.ps1`.

Default audio mastering is an explicit high-pass/compressor plus two-pass loudness targeting -14 LUFS and -1.7 dBTP, followed by AAC stereo 48 kHz. This is a studio choice, not an asserted Instagram rule. For approved existing AAC audio choose `-AudioMode copy`; do not repeatedly compress/master it. `-Encoder cpu` uses x264 slow CRF18 for `balanced` (~69 MB per 80 s, VMAF 98.3, about 2 minutes) and slow CRF16 for `max` (not separately measured). The old untuned p4 CQ20 `high` and CQ23 `compact` presets were retired.

A smaller H.264 file is lossy. Promise high visual quality, not mathematical losslessness or a universal percentage of retained quality. Preserve the original/master. For a true decoded-frame lossless video archive from a supported SDR video master, use `-LosslessArchive` and a fresh `.mkv` output (FFV1). It preserves the input pixel format and uses FLAC for audio; it is not the Instagram upload file. No prior compression is undone, and sample-format conversion of floating-point audio is separate from video losslessness.

## 7. Remotion and Concat limits

The bundled Remotion ffprobe crashes on this system; the dedicated compatible binary directory uses working system FFmpeg/ffprobe, which lacks libfdk_aac. Keep audio outside Remotion. OffthreadVideo also crashed in the FFV1 test, so replacing ffprobe alone does not repair every compositor use. Do not assert a complete Remotion repair. The installed regular Chrome completed 270 HTML5/H.264 captures, but the delivered sequence scored VMAF 93.25 with mistimed-frame outliers. This is not an approved footage fallback. Prefer frame-accurate native footage plus separately rendered custom graphics, and validate all new compositions. The wrapper uses regular Chrome because it launched successfully; this does not certify HTML5 frame selection. Do not turn on shared-memory capture with substituted generic FFmpeg binaries: that route depends on Remotion-specific support and needs its own correctness test.

The Concat FFV1/MKV roundtrip exposed frame-cadence mismatch on this millisecond-timebase test. The H.264/MP4 roundtrip completed in 21.82 seconds, with mean VMAF 98.205 against its input, while the browser test took 111.38 seconds for capture alone. These are simple-video tests, not equivalent full creative edits; do not generalise one format's result to every source. Retain exact source-to-output timing and inspect transitions. Do not transcode an already approved delivery repeatedly just to make another tool report GPU usage.

## 8. Verify the exact output

Check codec/profile, dimensions, fps, progressive scan, colour tags, decoded frame count, duration, start/end, missing/repeated frames, black frames, subtitles/safe areas, transitions and audio sync/loudness. Decode the whole delivery with FFmpeg `-xerror`. Inspect real moving playback and listen; still frames and ASR do not establish full audiovisual review. Use VMAF/SSIM as supporting measurements against aligned same-frame references; normalise timebases by decoded frame index for compression comparisons. Never hide real cadence errors by realigning away missing frames. VMAF is not a percentage of retained quality or a guarantee for phone viewing.

For true lossless archive verification, compare hashes of decoded frames at the same pixel format. Keep technical results and visual-review limits with the actual versioned file. Record total and stage time separately; a 90% faster final encoder does not mean the entire editing job is 90% faster.

## 9. Revision invalidation and the render handoff

Before a full render, record a short `Project/.context/RENDER.md`: source identity and retained ranges, cut revision, explicit colour/geometry/matte state, selected engine and reason, frame rate/dimensions, cache keys, approved audio source, final encoder profile, versioned destinations, sample results, QA still pending and next action. Update it when a relevant setting changes. It is a plan/receipt pointer, not proof that a file has been rendered.

| Changed item | Recompute | Retain only if identity still matches |
|---|---|---|
| New recording | Content, transcript, take/cut plan, colour/masks, cues and QA | Installed software/models and chosen technical delivery format |
| Cut, order or speed | Source-to-output map, dependent captions/graphics/audio, export and QA | Source transcript and grades whose source ranges/state remain valid |
| Colour/mask/lighting decision | Affected graded shots, dependent composite/export and QA | Approved cut and unaffected raw-asset analysis |
| Caption wording/layout or a graphic | Affected graphics/composite, export and visual QA | Approved source grade and cut timing if unchanged |
| Audio only | Mix/mastering, mux and audio/sync QA | Copy approved video packets; avoid a picture re-encode |
| Encoder/delivery format only | Delivery encode and exact-file QA | Approved current-job master/cache |
| Tool/model/helper version | Any stage whose cache identity includes it | Unaffected stages with independently valid identities |

CPU matting and GPU colour are different choices. GPU encoding does not accelerate ASR, masks, Python loops or browser capture. Profile those stages separately. Never repeat a lossy final encode just to make Task Manager show GPU activity.

## 10. Exact local command recipes

Paths containing CURRENT, APPROVED or NEW are placeholders. Resolve the actual current project and use fresh output names. These commands do not infer a look, select the latest old video or decide which mix is approved.

### Approved SDR master to high-quality Instagram delivery

```powershell
. 'E:\Video\scripts\env.ps1'
& 'E:\Video\scripts\Export-Instagram.ps1' -InputFile 'E:\Video\projects\CURRENT\work\APPROVED-master.mov' -AudioFile 'E:\Video\projects\CURRENT\work\APPROVED-premix.wav' -OutputFile 'E:\Video\out\NEW-instagram-v1.mp4' -Encoder nvenc -Quality balanced
```

This requires an explicitly prepared 1080x1920 30 fps SDR master. It does not silently resize, change fps, transform HDR or guarantee an MB budget. Preserve the master. If the selected input already has approved AAC audio, omit `-AudioFile` and use `-AudioMode copy`; picture is still encoded in this delivery operation.

### Already rendered PNG frames to one delivery encode

```powershell
& 'E:\Video\scripts\Export-Instagram.ps1' -InputFile 'E:\Video\projects\CURRENT\work\APPROVED-frames' -Frames -AudioFile 'E:\Video\projects\CURRENT\work\APPROVED-premix.wav' -OutputFile 'E:\Video\out\NEW-instagram-v1.mp4'
```

The directory must contain a contiguous, equally padded `element-NNN.png` sequence. It is interpreted as 30 fps, checked at 1080x1920; an explicit audio input is required. Do not introduce PNG intermediates when native processing already handles the footage correctly. Retain useful existing frames for same-job revisions.

### Custom Remotion graphics

```powershell
& 'E:\Video\scripts\Render-DirectorProject.ps1' -EntryFile 'E:\Video\projects\CURRENT\src\graphics.tsx' -Composition 'CURRENT_GRAPHICS' -Audio 'E:\Video\projects\CURRENT\work\APPROVED-mix.wav' -FramesDirectory 'E:\Video\projects\CURRENT\work\NEW-frames' -Output 'E:\Video\out\NEW-graphics-v1.mp4'
```

This captures PNGs with installed regular Chrome/concurrency2 and uses the direct exporter. It does not repair the known OffthreadVideo crash or HTML5 footage timing issues. Use only a composition whose relevant frame timing/pixels are verified. Prefer native frame-accurate footage plus independently checked graphics where practical. A standalone graphics render is not automatically an alpha overlay; choose and validate transparency/compositing separately. Do not auto-rewrite a live project's composition.

### Default colour + cut render (cut-first timeline renderer)

```powershell
& 'E:\Video\.venv\Scripts\python.exe' 'E:\Video\scripts\render-timeline-colour.py' 'E:\Video\projects\CURRENT\work\CURRENT-timeline-colour.json'
```

The config lists the edit's source segments ({in, frames}) and every colour parameter explicitly, plus `aroll` {encoder nvenc, quality 10, gop 30} for the graphics timeline (NVENC const-QP 10 measured 51.1 dB vs lossless, equal to x264 CRF8 and 24% smaller). Add `archive` only when a 16-bit FFV1 copy is really needed (it costs CPU and ~7.7 MB per frame). First render a ~10 s parity sample against an approved reference. Compare quality by decoded frame index: ffmpeg's psnr/ssim filters pair frames by timestamp, and an audio-muxed MP4 starts with an offset. Details and measurements: plans/TIMELINE-RENDERER-v1.md.

### Legacy full-length colour cache / parity reference

```powershell
& 'E:\Video\.venv\Scripts\python.exe' 'E:\Video\scripts\render-colour-fast.py' 'E:\Video\projects\CURRENT\work\CURRENT-reviewed-colour-job.json'
```

Supply the complete current-job configuration described in section 4. Only the tested HLG BT.2020/Hable/Rec.709, 1080x1920 module interface is supported. The lab JSON holds old v11 creative settings and must not be used for a new recording or the different v12 grade. GPU numerical parity must be checked when the job/module changes.

### Audio-only revision of an approved H.264 picture

```powershell
& 'E:\Video\.venv\Scripts\python.exe' 'E:\Video\scripts\master-delivery.py' 'E:\Video\projects\CURRENT\work\APPROVED-picture-with-premix.mkv' 'E:\Video\out\NEW-audio-v1.mp4'
```

This copies a compatible H.264 picture and masters its existing audio. It does not take a separate external mix argument. To replace audio, mux that approved picture with the new mix using explicit stream maps first, then master if needed. This helper has its own stronger compressor and AAC192k choices; use `--no-compress` for an already compressed mix when appropriate. Do not accidentally master approved audio twice. The normal final exporter uses its own documented audio chain/AAC320k. Both target -14 LUFS/-1.7 dBTP and require post-encode measurement.

### CPU fallback, archive and compatible joining

Use `-Encoder cpu -Quality balanced` explicitly if NVENC fails or a measured CPU route is preferred; record the reason. Never silently claim a GPU result after CPU fallback. `scripts/master.py` is a compatibility entry point for the current exporter, not the old software re-encode recipe.

Use `-LosslessArchive` with a fresh `.mkv` output from a supported SDR video master for FFV1 archival. Do not combine it with `-Frames`. This preserves the supported decoded video pixel format, does not undo prior losses, and may create a much larger file. Compare decoded-frame hashes if claiming identity. Video and audio losslessness are separate boundaries.

FFmpeg concat is distinct from the Concat app. For compatible already approved segments and a validated file list, `ffmpeg -nostdin -n -f concat -safe 0 -i LIST.ffconcat -c copy NEW.mp4` avoids encoding. Verify codecs/parameters, timebases, keyframes, timestamps, duration and seams. Arbitrary precise cuts, different streams or effects may need encoding; do not call a stream copy frame-accurate without checking it.

## 11. Installed tool map and when to use each

| Tool/helper | Installed location or selection | Use and boundary |
|---|---|---|
| FFmpeg / ffprobe | Existing system executables on PATH after env.ps1 | Probe, controlled filtering, native composition, mux, encode, decode and metrics; no new C: installation |
| Cut-first timeline renderer | scripts/render-timeline-colour.py | Default colour + cut route: one CuPy colour process, CPU matting workers, NVENC a-roll. hevc_nvenc does not open on this GTX 1650 |
| NVENC H.264 | Existing GTX1650 via export-instagram.py | Final GPU encode; not GPU colour/matting/capture, and not mathematically lossless MP4 |
| CPU x264 | Exporter `-Encoder cpu` | Explicit fallback: slow CRF18 (`balanced`, smallest measured file) or slow CRF16 (`max`) |
| CuPy 14.2 | tools/cupy-gpu, loaded by scripts/studio_gpu.py | Explicit compatible float32 colour math; 768 MiB pool limit is not total GPU usage |
| CPU ORT / RVM | Shared .venv; models/rvm/rvm_mobilenetv3_fp32.onnx | Current measured people-matting route, sequential recurrent state; reset/handle shot boundaries deliberately |
| CUDA ORT 1.26 | tools/onnx-gpu and tools/onnx-gpu-cuda | Isolated research option; tested matting configuration was slower, no automatic production switch |
| U2NETP | models/u2netp/u2netp.onnx | Image/general-object masks via remove-background.py; framewise video can shimmer |
| Concat 0.2.8 | tools/Concat-0.2.8/concat.exe; Start-ConcatMcp.ps1 | Native editable timeline and DX12 drawing; MCP headless project locking and format-specific QA; H.264 prefers CPU x264 |
| Remotion 4.0.537 | projects/renderer | Necessary custom graphics with installed regular Chrome; video decoder/capture limitations still apply |
| Compatible Remotion binaries | tools/remotion-native-4.0.537 | Working substituted FFmpeg/ffprobe; no libfdk_aac or automatic shared-memory compatibility |
| HyperFrames / Herk | Existing renderer dependencies; pinned repos/free247editor/kit | Existing composition/simple-edit routes, not measured as universally faster than native processing |
| Local speech transcription | scripts/transcribe.py and installed model cache | Source-timed words; verify names/numbers against audio; do not re-transcribe unchanged audio on every visual revision |
| Manual image/video prompting | /request-video-assets, /image, /video | User generates manually; request only useful assets, track filenames and handles, inspect returns |
| Gemini visible-mark processing | scripts/Remove-GeminiWatermark.ps1; D:/gemini-watermark-remover | Supported visible marks only; preserve originals/provenance and inspect results; no invisible-provenance claim |
| Background removal | scripts/remove-background.py | Explicit SDR/size/fps, preview first, asset preparation rather than unnecessary whole-video masking |
| Audio-only mastering | scripts/master-delivery.py | Copy an already compatible picture while changing audio; no external-mix parameter |
| Context and hooks | scripts/project-context.py, scripts/claude-context-hook.py | Small stage handoffs, render notes, checkpoints; no automatic editorial decisions or guaranteed token saving |
| Native encoder smoke test | scripts/Render-Test.ps1 | Synthetic pattern/tone only, fresh files; does not certify browser capture, colour taste, hair detail or a creative edit |

## 12. Readiness and evidence

Keep these states separate: installed; callable; representative sample passed; full render completed; whole-file technical decode passed; moving playback/listening reviewed; platform upload checked. A source file or an installed package is not evidence of a completed stage. Preserve prior benchmark measurements as dated evidence, without pretending the current composition or a new video passed those tests. Use `plans/CLAUDE-FILE-MAP.md` to locate the needed instructions.
