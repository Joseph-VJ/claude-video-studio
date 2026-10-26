---
name: remove-background
description: "Remove image or video backgrounds locally using U2NETP for images, recurrent RVM for people video, and existing FFmpeg, with all processing on E:."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->

The measured CUDA-ORT matting setup was slower here: retain the shared CPU RVM route. CuPy colour and NVENC encoding are separate stages. Low-resolution previews do not certify final-resolution masks; set size/fps deliberately and retain recurrent state within a shot.

Load E:/Video/scripts/env.ps1. Run E:/Video/.venv/Scripts/python.exe E:/Video/scripts/remove-background.py --help.
Image: image --input INPUT --output NEW.png
People video preview: video --input INPUT --output NEW.mp4 --mode composite --background '#202020' --seconds 2 --max-side 640
People video alpha: video --input INPUT --output NEW.webm --mode alpha
Video matte: video --input INPUT --output NEW.mkv --mode mask
Use a 2-second preview first. Reuse the loaded model for all frames; stream through RAM rather than dumping frame sequences.
Default video output is 30fps CFR, max-side 1280; these are explicit conversions. Request --fps/--max-side as needed. Source rotation is auto-applied by FFmpeg. SDR 8-bit only: normalize HDR separately before processing.
Preserve the source. Validate hair, glasses, hands, fast edges and motion. Video defaults to RVM MobileNetV3, which maintains recurrent state across frames and predicts foreground plus alpha for PEOPLE. Process one continuous shot per run; reset state by starting a new run at each scene cut. For general objects use --model u2netp, which is framewise and may shimmer. Both can fail on fine or transparent details. Do not promise production-quality keying from a simple test.
Keep audio through the wrapper's optional original audio mapping. Store output and its QA JSON in the current project's assets/processed. Check transparent WebM using FFmpeg libvpx-vp9 decoding; many players hide alpha.
No image/video upload or paid API is needed.

Tested smoke outputs: image alpha, 6-frame static-source transparent WebM, replacement-background MP4 and FFV1 matte, including retained test audio. Real human hair, motion, HDR and long-clip quality remain unverified.

The installed RVM FP32 model is about 15 MB and runs on the existing CPU ONNX Runtime. No Torch installation. It is person matting, not identity tracking: multiple people may all be retained. Do not promise real-time 1080p performance on this PC.
