# Rendering speed review — 25 October 2026

Scope: review the supplied rendering summary against the current IMG_2442 v12 scripts, saved receipts, stage log, output metadata and primary documentation. Preserve the creative treatment, EDL, source media, existing caches, masters and deliveries. This review is not a new edit or a claim that v12 received full moving-picture/listening QA.

## Verified production baseline

`projects/img2442-motion-v1/work/pipeline-v12g.log` records 3,089 seconds (51m29s). The timestamps and differences reconcile:

| Stage | Seconds | Share |
|---|---:|---:|
| Colour, three jobs | 1,408 | 45.6% |
| Physical FFV1 join | 414 | 13.4% |
| 28 cut encodes plus another joined encode | 651 | 21.1% |
| Build graphics / Remotion ProRes master | 589 | 19.1% |
| Premix and delivery | 27 | 0.9% |

The final exporter receipt records 22.482 seconds inside the last stage. Further final-encoder tuning has little effect on this baseline. The old nine-second sample's 89.6% encoding-time reduction does not apply to the complete job.

The existing v12 MP4 probes as H.264/yuv420p, 1080x1920, 30/1 fps, Rec.709, 2,388 frames / 79.6 seconds, with AAC audio and 137,637,271 bytes. These are metadata checks, not full audiovisual approval.

Three existing colour chunks total 20,633,198,986 bytes. The physical join writes another approximately 20.64 GB without changing picture content. Avoiding that join and replacing the recut stage addresses 1,065 seconds of old stage time, **before accounting for replacement assembly cost**; this is not a promise of 17m45s saved.

## Research audit

- The documented 19 URLs, 13 source groups and six GitHub repositories reconcile. These are not a recoverable historical query count. The 61-file category counts also add up; this review did not redo a content-by-content synchronization of all 61 files.
- The saved encoder/size percentages reconcile with their benchmark receipts. Short stage tests and file-size changes do not establish complete-job performance or identical pixels.
- GTX1650 H.264 NVENC support is consistent with [NVIDIA's matrix](https://developer.nvidia.com/video-encode-decode-support-matrix). Encoder-generation differences between GTX1650 variants matter for other feature claims.
- Correction: [Remotion shared-memory capture](https://www.remotion.dev/docs/shared-memory-capture) explicitly excludes Windows. Installing compatible binaries alone does not enable it here. Windows still captures ordinary JPEG/PNG screenshots.
- [Remotion hardware acceleration](https://www.remotion.dev/docs/hardware-acceleration) on Windows supports H.264/H.265 encoding; it does not GPU-encode the current ProRes4444 master or remove browser capture work.
- [Concat releases](https://github.com/jub0t/Concat/releases) still identify 0.2.8. Saved inspected source prioritizes libx264 for desktop H.264. Its DX12 compositor and its encoder are different stages; do not promote the failed FFV1 input path.
- Installed CuPy14.2 package metadata accepts NumPy>=2.0,<2.6; the installed NumPy2.5.4 fits. [CuPy's online tested-version list](https://docs.cupy.dev/en/stable/install.html) is narrower; it is not a reason by itself to downgrade a measured working environment.
- [ORT CUDA documentation](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html) now distinguishes CUDA13-default packages at 1.27+ from CUDA12 variants. Keep the existing isolated configuration pinned until a deliberate compatibility/performance test. CPU RVM remains the locally measured choice.
- The historical FFmpeg filter/specification URLs timed out during this review. Their successful live verification is not claimed. The existing FFV1 decoded-hash result remains evidence of that tested boundary only.

## Current architecture and next priorities

1. Read the existing lossless chunks through a validated source/frame map and assemble the edit with one encode. This avoids the physical join and 28 temporary H.264 clips plus their extra encode. Keep original audio as a separately mapped EDL input; validate AAC timestamp offsets and every cut.
2. Optimize the actual v12 colour function. Worker receipts show colour accounts for about 57% of aggregate worker time, CPU matte about 20%, read about 15%, and write about 8%. Its repeated float64 cumulative-sum blurs are a specific target; reducing bit depth or dithering would change picture and is a different decision.
3. Measure one/two/three colour workers after any kernel change. Three processes sharing a 4GB GPU, six logical CPUs and one disk need not be optimal. Do not combine timings from resource-competing benchmarks.
4. For graphics revisions, reuse matching colour/assembly caches. Longer-term, render reusable graphics independently and composite native footage, but preserve all CSS transforms, vignette, split transitions, flashes, AI-video frames and text timing. A transparent-overlay redesign needs its own visual parity work.
5. For audio-only revisions, preserve compatible approved H.264 video packets and process/mux audio. For delivery-only changes, use the existing approved master. No repeated transcription or colour pass is needed when its dependencies are unchanged.

## Cache identity correction applied

`scripts/render-colour-fast.py` now records the actual loaded static mask's shape, dtype and SHA256 in its cache identity before moving it to CuPy. Previously a change to the external mask image could leave all recorded Python dependency hashes unchanged. This changes identity bookkeeping only; colour arithmetic, masks, parameters and rendering commands are unchanged. Existing cache files and receipts were retained. The previous adapter is backed up under `work/render-speed-review-20261025/`.

Syntax validation passed and an independent review found no picture-behavior change. Future colour-render receipts include the mask identity; old receipts must not be retroactively described as containing it.

## Limits

No source, v12 grade parameters, production composition, source-to-edit word map or delivery was overwritten. No new packages, paid services or C: files were introduced by this review. The original Bash production launcher was inspected but not executed; new commands use the E:-only PowerShell environment. Production readiness must be decided from the exact new path's frame/audio/color results, not from the fact that an optional helper exists.
