# Render speed research and measured results — v1

2026-10-25. Requested work: research official documentation/GitHub, make rendering faster on this PC, reduce Instagram upload size while preserving visual quality, and give Claude a usable workflow. All new tools, downloads, caches, benchmarks and outputs are under E:/Video. Existing C: FFmpeg is reused. No driver, system-wide CUDA toolkit, OS setting, old project grade or active-project pointer was changed. The in-progress v12 edit was not modified.

## Applied changes

1. Added isolated CuPy CUDA colour compute with a strict current-job configuration adapter. It preserves the reviewed float32 colour calculations; no automatic float16 conversion or lighter look was introduced.
2. Fixed the Windows high-resolution raw-pipe allocation problem in that adapter: reuse a preallocated frame buffer with `readinto`, instead of allocating the remaining multi-megabyte frame size on each small pipe read.
3. Added a measured H.264 NVENC high-quality delivery exporter, including separate audio mastering, an explicit CPU fallback and technical output checks.
4. Added direct contiguous-PNG-to-NVENC delivery. The Remotion wrapper no longer makes an intermediate H.264 encode before final delivery; it retains PNG frames as the cache.
5. Added a distinct FFV1 video archive option, checked by decoded-frame hashes. Upload MP4 and true lossless archival have separate purposes.
6. Added source/configuration/dependency/model/runtime cache identities to colour outputs. Cache reuse remains deliberate and job-specific; there is no automatic reuse of another video's treatment.
7. Installed `/video-render-fast`, saved the detailed Claude workflow and updated CLAUDE.md, the runtime reference and /video-director to use it.
8. Tested Concat native composition, Remotion paths, CPU/CUDA matting, NVDEC, multiple encoder presets, numerical parity, whole-file decoding and audio loudness. Slower or incorrect routes were not made automatic defaults.

## What was slow

The existing colour render combined two high-precision HLG-to-SDR exposure variants, full-resolution NumPy corrections, CPU RVM matting and software x264 encoding. Six processes did not remove these serial costs. The old recut also encoded cuts and then encoded a join again. Browser frame capture and x264 `slower` finishing added further work. Filling RAM or setting a thread count cannot remove those stages.

The important new finding was the unbuffered pipe reader. On Windows it repeatedly requested the entire remaining frame allocation even when the pipe supplied small pieces. The replacement keeps one frame buffer. The CPU output before/after this change was bit-identical across all 12 tested frames.

## Hardware and benchmark conditions

AMD Ryzen 5 3500, 6 cores/6 threads; approximately 32 GB RAM; NVIDIA GTX 1650 4 GB, driver 610.88; native FFmpeg 8.1; shared Python 3.12.13 / NumPy 2.5.4; Remotion 4.0.537; Concat 0.2.8. These are single-machine measurements, with background host activity uncontrolled. They are evidence for route selection, not a guaranteed total-job speedup.

The source benchmark uses IMG_2442.MOV: HEVC 10-bit HLG BT.2020, rotated portrait, 30 fps. The existing v11 ProRes graphics master was reused only as a measurement/export source. It remains intact. The benchmark grade/settings are specific to that old video and must not become a new-video preset.

## Encoder comparison

A common 9-second reference contains three 3-second sections beginning at 0, 25 and 65 seconds of the v11 master. It is normalised once to 1080x1920, 30 fps, SDR Rec.709 limited, 8-bit 4:2:0 and stored with lossless FFV1. The table measures video encoding only, excluding reference creation, metrics and audio.

| Encoder case | Seconds | Decimal MB | Mean VMAF | Mean float SSIM |
|---|---:|---:|---:|---:|
| x264-slower-crf10 | 51.395 | 24.30 | 98.913 | 0.999668 |
| nvenc-p4-cq16 | 5.524 | 25.98 | 98.890 | 0.999608 |
| nvenc-p5-cq18 | 7.122 | 20.21 | 98.793 | 0.999508 |
| nvenc-p5-cq16 | 5.152 | 26.06 | 98.888 | 0.999609 |
| x264-fast-crf16 | 14.084 | 10.82 | 98.380 | 0.999110 |
| nvenc-p5-cq20 | 6.569 | 15.22 | 98.647 | 0.999346 |
| nvenc-p4-cq20 | 5.359 | 15.20 | 98.650 | 0.999341 |

(Superseded later on 2026-10-25: the default is now `balanced` = NVENC p7 tuned CQ24, about 38% smaller again with no visible difference; see plans/TIMELINE-RENDERER-v1.md. The text below is the original dated result.) Selected default at the time: NVENC p4/hq, VBR CQ20, spatial AQ 8, maxrate 24M, bufsize 48M, GOP60. Versus the matched x264 slower/CRF10 test, it took **89.6% less time (9.59x speed)** and produced a **37.4% smaller file**. The higher-bitrate CQ16 files were fast but did not meet the smaller-file goal. CPU fast/CRF16 is an available explicit fallback, with a measurable quality/size trade-off.

VMAF 98.65 is not “98.65% of the quality.” These metrics compare compression after intentional 8-bit/chroma delivery conversion. They do not establish identity with the original HDR/ProRes frames, and they do not certify every fast-motion/noisy source or Instagram's own subsequent transcode. Default VMAF's viewing assumptions also differ from vertical phone viewing.

Metric alignment matters: initial JSON files without `aligned` in the first five cases used mixed MKV/MP4 timebases and gave misleading scores. The final results were recomputed with both streams normalised to `settb=1/30,setpts=N`. Use the updated aggregate JSON and `*.aligned-vmaf.json`; the last two CQ20 cases already use corrected alignment. The benchmark script itself has been fixed. Historical unaligned files are retained as diagnostic evidence, not valid final quality results.

## Full existing-master export

- New file: `E:/Video/out/IMG_2442-v11-nvenc-quality-v1.mp4`.
- Export elapsed time: **31.268 seconds**, including audio measurement and delivery encoding, from the already-rendered master. This is not the entire edit/grade/graphics render time.
- New size **137.84 MB**, previous v11 MP4 **229.51 MB**: **39.9% smaller**. The separate existing `v11-small` file was not the comparison baseline and was not overwritten.
- Verified 2388 decoded video frames, 79.600 seconds, 1080x1920, 30 fps, progressive High-profile H.264, 8-bit 4:2:0, Rec.709 limited; AAC stereo 48 kHz. Full video/audio decode completed with FFmpeg `-xerror` and no reported decoder errors.
- Post-encode audio measured approximately -14.04 LUFS integrated and -3.25 dBTP. The true-peak target is a ceiling, not a demand to raise the peak to that number.
- Master/delivery full-frame and detailed still comparisons were inspected at 25.5 seconds, including skin, hair, graphics edges and captions. They appeared close in the inspected images. This does not constitute continuous full playback/listening review or an Instagram upload test.

## Colour and pipe results

All integrated rows below produce 12 full-resolution frames at source time 12 seconds, with identical explicitly supplied parameters, CPU RVM matting and 16-bit RGB FFV1 output. The test has dither strength zero and no temporal warm-up, consistently for both paths. Runtime/model import and cache identity construction are outside the stage timer. This is not a parity comparison with the historical dithered final video.

| Timed pipeline | Total seconds | Frame read seconds | Colour seconds | CPU matte seconds |
|---|---:|---:|---:|---:|
| CPU colour, original reader | 92.046 | 55.727 | 31.511 | 3.600 |
| CPU colour, fixed reader | 41.168 | 2.748 | 33.201 | 3.904 |
| GPU colour, fixed reader | 10.955 | 2.863 | 2.843 | 4.024 |

Combined, the tested pipeline took **88.1% less time (8.40x speed)** than its original CPU/reader version. GPU vs CPU after the common reader fix is about 3.76x. These are short sequential stage tests, not a full-length, six-worker, end-to-end comparison.

The isolated warmed colour function's median fell from 2.507 to 0.106 seconds per full-resolution frame, approximately 23.7x; the first GPU call included about 14.8 seconds of kernel compilation. Those function-only numbers exclude decode, matting and encoding. The integrated GPU/CPU decoded FFV1 frames differed in only 4132 of 74,649,600 RGB channel values, by at most **one 16-bit code value**. Buffer-only CPU output was bit-identical. See `integrated-colour-parity.json`.

Separate 6-frame decode-to-null tests were approximately 1.39 s CPU/default, 1.48 s CPU/filter2 and 1.48 s NVDEC/filter2; the raw E: file test was 1.39 s. Decode itself was not the 56-second read bottleneck. NVDEC is not automatically enabled on this evidence.

## Matting and CUDA outcome

The isolated CUDA runtime was made functional using pinned CUDA 12 components, cuDNN 9 and an explicit DEFAULT convolution search setting. HEURISTIC mode initially failed and could fall back to CPU; those early attempts are not counted as successful GPU performance evidence. The wrapper disables runtime provider fallback and checks active providers. Some operator/shape work may still use CPU as part of normal graph placement.

On 24 actual, 360x640 source frames with the same downsample ratio, the shared CPU ORT 1.31 configuration took 1.71 s inference (~0.0696 s/frame warm), while the tested CUDA EP ORT 1.26 configuration took 8.08 s (~0.3104 s/frame warm). Masks were numerically close. Runtime versions and execution configuration differ, so this is not a universal hardware comparison. Full-resolution CUDA/IO-binding tuning could behave differently and was not certified here. Current production choice: **CPU RVM matting and CuPy colour**, with no matting-quality reduction.

## Concat and Remotion outcomes

| Test | Time | Outcome |
|---|---:|---|
| Concat GPU compositor, FFV1/MKV reference, H.264 fast/CRF16 export | 32.08 s | 270 frames; mean VMAF 85.93, cadence mismatches. Not approved as a frame-identical route for this input. |
| Concat GPU compositor, exact-timebase H.264/MP4 input, same native export setting | 21.82 s | 270 frames; mean VMAF 98.205, minimum 95.112. Suitable evidence for this simple native route, subject to real-project QA. |
| Remotion OffthreadVideo, FFV1 input | Failed | Headless-shell startup timeout; regular Chrome started but the compositor crashed with 0xC0000005. |
| Remotion HTML5 H.264, regular Chrome, 270 PNG frames, concurrency2 | 111.38 s capture | Completed. Additional NVENC export 6.12 s. Mean VMAF 93.25 with low-scoring frame outliers: not promoted for frame-accurate footage without fixing capture/seek behaviour. |

These are straight-video tests, not equivalent complete creative edits. Concat's GPU DX12 drawing was verified in the native log. Its H.264 selection prefers libx264 even when a GPU is present; current source confirms this. GPU compositing and NVENC encoding are different. The MP4 native path is substantially faster than the tested browser path, but neither can be claimed universally fastest or automatically equivalent to the custom Python grade.

The FFV1/MKV cadence result is input-specific; millisecond timestamp quantisation is a plausible contributor, not a proven sole cause. The MP4 test avoids that particular input and scores well. Do not use frame realignment to conceal actual missing/repeated frames. Thumbnail diagnostics and per-frame VMAF are retained.

The practical architecture is native FFmpeg/Concat for ordinary footage and supported effects, and Remotion for the complex graphics that need it. Render and verify graphics separately where practical, then composite with the original frame-accurate footage. Do not assume the HTML5 fallback or substituted binaries repair every video path. Shared-memory capture is not promoted because it requires compatible Remotion support and a correctness test.

## Losslessness and QA safeguards

The Instagram MP4 is deliberately lossy, with measured high visual similarity. Existing originals/master are preserved. ProRes 4444 is an editing master format, not mathematically lossless. FFV1 archival mode preserves supported decoded input video frames/pixel format; it does not undo source compression or make a smaller upload guarantee. The 9-second archive test matched SHA256 hashes for **all 270 decoded video frames**. Its output was ~170 MB versus the selected MP4's ~15 MB, illustrating the size trade-off. Float PCM -> FLAC audio sample representation is separate from video losslessness.

The exporter refuses existing outputs, paths outside E:/Video, implicit resize/frame-rate changes, direct HDR-to-SDR retagging, unexpected output pixel format for archival, output duration/fps mismatch, and discontinuous PNG numbering. Existing-output and unprepared-HDR guard checks passed without modifying output files. The PNG bridge produced exactly 30 video frames/1 second with AAC; explicit CPU export plus AAC copy was also tested. Audio-only approved revisions should copy video, avoiding another picture encode.

Visual review of all moving output and an actual Instagram transcode remain separate from these technical checks. A complete new creative project and a full-length accelerated colour job have not been rendered by this optimization task.

## Installed components and footprint

New isolated packages: CuPy CUDA12x 14.2.0, fastrlock 0.8.4, cuda-pathfinder 1.8.4, ONNX Runtime GPU 1.26.0, CUDA runtime 12.9.79, cuFFT 11.4.1.4 and nvJitLink 12.9.86. Existing shared cuBLAS/cuDNN/NVRTC are reused. CPU ONNX Runtime remains installed and is the matting default. No PyTorch, full CUDA toolkit or extra desktop editor was installed.

| New target/cache | Size at measurement |
|---|---:|
| `E:\Video\tools\cupy-gpu` | 147.00 MiB |
| `E:\Video\tools\onnx-gpu` | 362.14 MiB |
| `E:\Video\tools\onnx-gpu-cuda` | 368.34 MiB |
| `E:\Video\cache\cupy` | 0.20 MiB |
| `E:\Video\cache\cuda` | 1.62 MiB |

The three runtime targets total about 877.5 MiB, plus small GPU compilation caches. Pip downloads and benchmark evidence use additional E: space. These compiled GPU runtimes are larger than the tiny Claude instruction files; none were installed on C:. The unused-for-production CUDA matting target is retained as an isolated research option, not activated globally.

## Files and use

- `plans/FAST-RENDER-WORKFLOW-v1.md`: the operational guide for Claude, including new-video reset, route selection, cache rules, export examples and quality checks.
- `.claude/commands/video-render-fast.md`: installed slash command.
- `scripts/Export-Instagram.ps1` / `export-instagram.py`: master/PNG delivery, explicit CPU/AAC-copy options and separate FFV1 archival.
- `scripts/render-colour-fast.py`: explicit compatible current-job colour adapter, reusable pipe reader, cache manifest and CPU/GPU choices.
- `scripts/studio_gpu.py`: E:-local CUDA DLL setup and isolated imports; no global environment changes.
- `scripts/Render-DirectorProject.ps1`: existing interface plus encoder/quality/browser options; direct PNG delivery; prior helper saved alongside it.
- `projects/render-speed-lab-20261025`: original benchmark scripts, seven encoder cases, corrected quality metrics, raw diagnostics, provider logs, source provenance, parity, hashes, probes and compact `summary.json`.

Use `/video-render-fast` with the actual current project/master. Do not run lab jobs as a template for a new person/video. All new creative parameters must come from that video's content and reviewed settings.

## Primary-source research

The research covered the engine, codec, numerical compute, model, browser capture, validation and upload-boundary questions. Repositories were inspected for their role; cloning extra repositories was not treated as a performance improvement.

| Primary source / repository | Decision informed |
|---|---|
| [NVIDIA FFmpeg guide](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.1/ffmpeg-with-nvidia-gpu/index.html) | Distinguish NVENC/NVDEC, confirm FFmpeg capabilities and measure actual device paths. |
| [NVENC preset migration](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.0/nvenc-preset-migration-guide/index.html) | Benchmark preset/quality/rate-control choices instead of treating NVENC as x264 CRF. |
| [GPU codec matrix](https://developer.nvidia.com/video-encode-decode-support-matrix) | Capabilities depend on the actual GTX1650; an encoder listed by FFmpeg does not prove GPU support. |
| [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) and [FFV1 specification](https://ffmpeg.org/~michael/ffv1.html) | Explicit colour transforms, aligned metrics, filtering/encoding boundaries and true decoded-frame archival. |
| [Concat releases](https://github.com/jub0t/Concat/releases) and [source](https://github.com/jub0t/Concat) | Native DX12 export, MCP integration, encoder selection and version-specific tests. Source snapshot 971ad1d9214e85755c05edc8777c05b4d4e255dc; installed binary remains v0.2.8 / 79116bd. No experimental source build replaced it. |
| [Remotion hardware encoding](https://www.remotion.dev/docs/hardware-acceleration) | Windows NVENC support exists; it only accelerates encoding and must not be confused with browser capture. Local compatibility failures require separate tests. |
| [Remotion shared-memory capture](https://www.remotion.dev/docs/shared-memory-capture) and [repository](https://github.com/remotion-dev/remotion) | New capture path was considered, but substituted generic binaries and correctness concerns block automatic adoption. |
| [CuPy installation](https://docs.cupy.dev/en/stable/install.html) and [repository](https://github.com/cupy/cupy) | NumPy-like GPU operations, compatible wheels and smaller component installs instead of a whole system toolkit. |
| [ORT CUDA provider](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html) and [repository](https://github.com/microsoft/onnxruntime) | CUDA/cuDNN compatibility, provider options, fallback detection and possible future I/O binding. |
| [cuDNN support matrix](https://docs.nvidia.com/deeplearning/cudnn/backend/latest/reference/support-matrix.html) | Check support rather than assume an older card cannot run CUDA. Actual convolution configuration was the relevant local issue. |
| [RVM inference](https://github.com/PeterL1n/RobustVideoMatting/blob/master/documentation/inference.md) | Sequential recurrent states, explicit resolution/downsample choice and inference API; speed changes must preserve temporal behaviour. |
| [Netflix VMAF FAQ](https://github.com/Netflix/vmaf/blob/master/resource/doc/faq.md) and [models](https://github.com/Netflix/vmaf/blob/master/resource/doc/models_v0.md) | Metrics support comparison but have viewing assumptions and cannot prove mathematical losslessness or a retained-quality percentage. |
| [Meta's official Instagram API collection](https://www.postman.com/meta/instagram/overview) | API upload constraints are a distinct surface from organic app uploads; neither supplies a promise of no recompression. |

This report separates documented capabilities, measured results and remaining hypotheses. Use the workflow for operations and this evidence only when investigating a relevant stage.

## Instruction integration follow-up

The measured results above remain dated benchmark evidence. Current Claude instructions, commands, project handoffs, legacy entry points and the configuration bundle were synchronised in the separate update recorded in CLAUDE-RENDER-INTEGRATION-UPDATE-v1.md. Use CLAUDE-FILE-MAP.md for selective reading and FAST-RENDER-WORKFLOW-v1.md for operations. The new instruction/encoder smoke checks do not certify the current v12 creative edit.
