# Cut-first timeline renderer and smaller delivery — v1 (2026-10-25)

**Adopted as the studio defaults on 2026-10-25 at VJ's request:** colour + cuts render with this tool, and Export-Instagram's default preset is now `balanced` (NVENC p7 tuned CQ24). The old `high` (p4 CQ20) and `compact` (CQ23) presets were retired; `max` (tuned CQ20) remains for when a larger file is explicitly wanted. Full v12 check of the new default: 84.8 MB vs 137.6 MB, 2388 frames, VMAF 97.05 vs 97.49 for the old default (every 5th frame against the master; about 6 points is the usual visibility threshold).

Tool: `scripts/render-timeline-colour.py CONFIG.json` (the full-length `render-colour-fast.py` remains as the parity/reference tool).
For a NEW video: write that video's own colour module (same interface as render-colour-fast.py: R, MASK, luma, smoothstep, box_blur, correct) and its own reviewed parameters and segment list. Never copy IMG_2442's look or settings.

## What it does
Decodes only the edit's segments -> RVM matting in CPU worker processes (state reset at each cut, short warm-up) -> grades every frame in ONE GPU process (CuPy) -> encodes the edited a-roll directly (+ optional FFV1 16-bit archive) -> cuts audio with the same segments and muxes without touching picture. No full-length grade, no 20 GB chunk files, no physical join, no per-cut re-encodes.
Config keys are all explicit (no inherited defaults): input, segments [{in, frames}], grade_module (+module_sha256), parameters (every key in R), shirt_gains, width/height/fps (1080x1920@30 reviewed), preprocess (hlg-hable-bt709 only), compute gpu|cpu, fast_blur_float32, matte, matte_warmup_frames, matte_threads, decode_threads, cpu_workers, dither_strength (<=1/255), dither_seed, aroll {path, encoder x264|nvenc|nvenc-lossless, quality, gop}, optional archive {path}, optional audio {source, fade_ms, codec, bitrate}.
GPU kernels are compiled before the workers start (CuPy's library probe has a 10 s timeout under CPU load).

## Measured on IMG_2442 (344 edited frames, v12 look, GTX 1650 + Ryzen 5 3500)
| Run | Chain speed | Notes |
|---|---|---|
| Old v12 route (colour + join + 28-cut recut) | ~0.97 fps equivalent | 41 min of the 51.5 min job |
| t1 new renderer, x264 CRF8 | 2.34 fps | GPU colour 0.31 s/frame was the limit |
| t2 + float32 blur, GPU dither, writer thread, + FFV1 archive | 2.60 fps | CPU became the limit (x264 + FFV1 on CPU) |
| **t3 + NVENC const-QP 10 a-roll** | **3.18 fps** | GPU colour 0.25 s/frame is the limit |
| t4 NVENC lossless a-roll | 3.02 fps | High 4:4:4 Predictive profile: archive use only, not for Remotion |
Picture vs finished v12 a-roll: mean diff ~1/255; wall/face/suit/shirt means within 0.3 levels. A-roll quality vs lossless (frame-indexed): x264 CRF8 51.4 dB, NVENC QP10 51.1 dB (24% smaller), NVENC lossless 66.6 dB.
Comparison caution: ffmpeg's psnr/ssim filters pair frames by timestamp; an audio-muxed MP4 has a start offset, so compare by decoded frame index (or setpts=N/30/TB on both inputs).

## Projected whole job for an ~80 s Reel (estimate, not yet a full run)
Colour + cut a-roll ~12-13 min (was ~41) + Remotion graphics ~10 min (unchanged) + export 5 s-2 min = ~23-25 min (was 51.5).

## Delivery size test (15 s of the v12 master, video only, quality vs the master's own 8-bit 4:2:0)
| Option | 80 s video | VMAF / luma PSNR | Encode |
|---|---|---|---|
| Current Export-Instagram (NVENC p4 CQ20) | 141 MB | 98.9 / 49.1 dB | GPU, ~25 s |
| NVENC p7 tuned CQ22 (lookahead 32, temporal AQ, multipass, B-ref) | 117 MB | 98.7 / 48.6 dB | GPU |
| NVENC p7 tuned CQ24 | 89 MB | 98.4 / 47.7 dB | GPU |
| x264 slow CRF18 | 69 MB | 98.3 / 47.0 dB | CPU, ~2 min |
Zoomed (3x, nearest) face, text-edge and fabric crops showed no visible difference between master and all three smaller options. These are not mathematically lossless; keep the master. hevc_nvenc failed to open on this GTX 1650 (with and without B-frames); H.264 is used.
Instagram re-encodes uploads, so very large uploads do not keep more quality after posting.
