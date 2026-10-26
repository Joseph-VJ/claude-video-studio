# Local Windows video studio

Root: E:/Video. Start Claude with Start-DirectorStudio.cmd or Start-ClaudeVideo.ps1 so new state, models, caches and temporary outputs stay on E:. Existing C: executables are reused. The former root AGENTS.md was revoked; use CLAUDE.md and plans/CLAUDE-FILE-MAP.md for current instructions.

## Use the studio

Put a recording in raw/ and supply its exact path and intended result. Use `/video-director` to inspect content, audience and performance, plan the edit and make a versioned draft within the requested scope. `/video-render-fast` chooses current supported render paths and export settings. This is an agent-assisted workflow, not an unattended folder watcher.

Read [the file map](plans/CLAUDE-FILE-MAP.md) for the current stage and [the render workflow](plans/FAST-RENDER-WORKFLOW-v1.md) for exact commands. New footage gets fresh analysis, colour interpretation, grade, masks and cues. Existing edits retain their own approved treatment; old IMG_2442 settings and benchmarks are not new-video presets.

## Design that does not look AI-made

`/video-design` sets each project's on-screen design (`.context/DESIGN.md`: palette from the footage, type, surfaces, one icon system, motion grammar) before graphics are built, and `.claude/skills/video-design/scripts/design-audit.py` audits rendered frames for neon pixels, rainbow accents and banding risk. It refines the approved fresh-v1/v12 structure rather than replacing it.

## Current render routes

Use native FFmpeg/format-validated Concat for ordinary footage and supported effects; use Remotion/HyperFrames only for verified custom graphics that need them. GPU compositing and GPU encoding are different. Known browser footage crash/timing issues remain documented.

`scripts/render-timeline-colour.py` is the default colour + cut renderer (cut-first, one GPU colour process, NVENC a-roll; see plans/TIMELINE-RENDERER-v1.md). `scripts/Export-Instagram.ps1` exports an approved SDR 1080x1920 30 fps master or verified PNG cache with the `balanced` preset by default (NVENC p7 tuned CQ24, ~89 MB per 80 s), `max` on request, and an explicit CPU fallback. `Render-DirectorProject.ps1` sends graphics PNGs directly to the exporter. `master-delivery.py` performs compatible picture-copy/audio-only changes. `master.py` delegates to the current exporter. Avoid unnecessary intermediate H.264 generations.

Custom CuPy colour is available only through a reviewed compatible current-job configuration. CPU RVM remains the measured matting default. A small upload MP4 is lossy; preserve originals/masters, and use separate FFV1 archival when true decoded-video-frame losslessness is needed.

## Context, assets and checks

Each project keeps .context/STATE.md and RENDER.md with its source/cut/grade identities, stage/cache choices, pending assets, exact output and QA. Reuse only matching same-job caches. Claude asks for missing assets with /request-video-assets, /image and /video; the user generates manually. Check returned files and keep provenance.

Run `scripts/Check-DirectorStudio.ps1` for current presence/version checks; it saves logs/studio-doctor/latest.json. `scripts/Render-Test.ps1` makes a fresh synthetic native pattern/tone export and verifies 150 frames/full decode; it does not certify browser capture, a creative edit or moving human masks. Historical setup tests and render benchmarks stay under logs/, projects/ and the dated research report.

Current results: [render research](plans/RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md). Current integration changes: [Claude update record](plans/CLAUDE-RENDER-INTEGRATION-UPDATE-v1.md). Full audiovisual review and platform recompression are separate checks. No paid generation, publication or source upload is implicit.
