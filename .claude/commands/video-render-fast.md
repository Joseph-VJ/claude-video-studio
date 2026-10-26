---
description: Profile and export the current video with verified fast paths while preserving visual quality.
argument-hint: <current project or approved master, output name, optional brief>
---
Request: $ARGUMENTS

Read plans/FAST-RENDER-WORKFLOW-v1.md. Load scripts/env.ps1. Resolve the actual current project from this request and .context/active-project.txt; the render-speed lab is test evidence, never the default creative project.

List the concrete tasks before work. For a NEW video, inspect its content, metadata and representative motion first, then make a fresh source-anchored plan. Never inherit the previous video's grade, white balance, masks, graphics, cuts or colour-conversion settings. For an approved export, retain that project's approved treatment.

Time decode, matting, colour, motion and final encoding separately. Use FFmpeg for straightforward operations, compatible stream-copy concat for suitable unchanged streams, Concat for validated native effects, and Remotion for necessary custom graphics. Concat is the editor app; FFmpeg concat is a joining operation. GPU compositing does not establish GPU encoding.

Use scripts/Export-Instagram.ps1 for an explicit 1080x1920, 30 fps SDR master. Default Encoder nvenc and Quality balanced (NVENC p7 tuned CQ24, ~89 MB per 80 s, measured visually identical to the old CQ20 file); use Quality max only when the user asks for a larger file. It also accepts a contiguous PNG directory with -Frames and an explicit -AudioFile. Never silently resize, discard frames, retag HDR as SDR, reuse an old look, or claim an H.264 MP4 is mathematically lossless. Preserve the master. Use -LosslessArchive only when a true decoded-frame lossless FFV1 archive is needed and disk capacity is sufficient.

Default colour + cut route: scripts/render-timeline-colour.py with a CURRENT-JOB config (segments, colour module, every parameter explicit, aroll encoder nvenc quality 10). It grades only the edit's segments, mattes in CPU workers (state reset at each cut with warm-up), runs ONE CuPy colour process and writes the edited a-roll directly, so there is no full-length cache, join or per-cut re-encode. Render a ~10 s parity sample first and compare by decoded frame index. See plans/TIMELINE-RENDERER-v1.md. The older full-length adapter scripts/render-colour-fast.py is kept as the parity/reference tool; it requires a reviewed CURRENT-JOB colour module, all explicit parameters, current mask geometry and source metadata. Lab configurations contain an old video's settings and are not templates. Validate CPU/GPU parity on representative footage before the full job. It uses a reusable pipe buffer and CPU RVM matting; CUDA matting was slower in this machine's tested configuration. No automatic GPU matting switch or model-quality downgrade.

Cache within the current job, with matching source SHA256, parameters, module dependencies, models, geometry, timing and runtime identity. Reuse only matching results. Change only affected stages; audio-only changes copy picture. Preserve source recordings and editable projects. Save stage timings, tool settings, exact output and QA limits to the current project's context. Check frames, duration, colour, motion, captions and audio before calling it ready. No publication is implicit.

Local browser footage tests failed the frame-timing quality gate despite completing PNG capture. Do not treat HTML5 video capture as an approved fallback. Prefer native frame-accurate footage with separately verified motion graphics. See the report for format-specific Concat results.

<!-- studio-render-integration:v1 -->
For applicable video work use E:/Video/plans/CLAUDE-FILE-MAP.md and the current stage of E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Keep the current project's .context/RENDER.md. Derive fresh creative settings/masks for new footage; same-project caches require matching identity. Native footage, verified graphics, one deliberate delivery encode and exact-file QA govern older upstream recipes.
<!-- /studio-render-integration:v1 -->
