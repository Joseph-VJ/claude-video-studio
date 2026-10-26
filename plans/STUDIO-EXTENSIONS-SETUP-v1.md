# Claude Video Studio Extensions — installed

> Dated installation record: the setup/test facts below describe their original date. Current render operations, known browser limitations, GPU colour/NVENC paths and cache rules are in [FAST-RENDER-WORKFLOW-v1.md](FAST-RENDER-WORKFLOW-v1.md). Use [CLAUDE-FILE-MAP.md](CLAUDE-FILE-MAP.md) for current entry points. Old sign-in/tool test snapshots are not a fresh status check.
Date: 24 October 2026

All new installations, configuration, models, test outputs and studio caches are on E:. The pre-existing Gemini remover remains at D:/gemini-watermark-remover; its source and dependencies were not modified. Existing Claude/FFmpeg executables on C: are reused.

## Start
Double-click E:/Video/Start-DirectorStudio.cmd.
Sign in once in this dedicated E: Claude profile. Native auth status currently reports loggedIn=false, configDirectory=E:/Video/cache/claude and projectsDirectory=E:/Video/cache/claude/projects.
These redirects apply when using the studio launchers; they do not relocate Windows, unrelated applications, other launch methods or hardcoded third-party paths.

## Six new direct Claude skills
Installed in E:/Video/.claude/skills; 19 existing skills remain discoverable through small forwarding guides pointing to their unchanged original E: folders. The old skills junction is retained as .claude/skills-legacy for compatibility.
- /studio-context — initialize, checkpoint and resume per-project notes.
- /request-video-assets — source-anchored requests, prompts, filenames, incoming assets and QA.
- /image — copy-ready still-image prompts for manual generation.
- /video — copy-ready video prompts, continuity and editorial handles.
- /gemini-clean-assets — existing local Gemini image/video remover.
- /remove-background — image cutouts, recurrent people-video matting and general-object video segmentation.

The image/video reference libraries come from smixs/visual-skills, commit 92be33a5a73325fb3d8e0c73b22744b114e2a90e, CC BY 4.0, author Serge Shima. Attribution/license files are included. Entry guides are locally adapted for manual generation, selective reading and verification of generator-specific capabilities.
Skill files total approximately 0.5 MB excluding their local Git history. No generation API/key is configured.

## Context and storage
- E:/Video/cache/claude: native Claude profile/session storage.
- E:/Video/.context/claude-memory: automatic memory, configured in the dedicated profile.
- E:/Video/cache/tmp and cache/claude-tmp: process temporary files.
- Project/.context/STATE.md: current goal, source anchors, stage, output, checks, missing assets and next action.
- Project/.context/DECISIONS.md: editorial decisions and reasons.
- Project/.context/ASSET-REQUESTS.md and manifest.json: asset status and output references.
- PreCompact copies existing small notes into project-local checkpoints.
- PostCompact saves the latest summary into LAST-COMPACT.md.
- SessionStart reminds Claude which project's state to read; no demo project is left active.
- Status line displays live context percentage and available session cost data.
- The large director plan is no longer an automatic @ import. Claude reads relevant sections when needed.
- Automatic Claude executable updates are disabled for the studio launch to avoid unexpected C: updates. Manual updates remain possible.
Use /context and /cost to inspect actual usage; checkpoint before /compact. Files cannot expand context limits or guarantee token savings.
Keep originals, credentials, models and active render directories. Inspect rebuildable caches before deleting them; no broad C: cleanup was performed.

Initialize a project:
```powershell
. E:\Video\scripts\env.ps1
& E:\Video\.venv\Scripts\python.exe E:\Video\scripts\project-context.py init --project E:\Video\projects\my-reel
```

## Manual generation handoff
Claude writes a request in Project/assets/requests, displays its prompt in chat and records the asset ID, timeline anchor, purpose, target size/duration, continuity, exact filename and acceptance criteria.
Generate manually in your chosen tool; save under Project/assets/incoming.
Claude can continue independent work with labelled placeholders. Required missing assets block claiming a final delivery.
On return, preserve the original, inspect the file, optionally remove a supported visible Gemini mark/background, save processed versions, update the manifest and replace the corresponding placeholder.
Examples: plans/GENERATED-ASSET-WORKFLOW.md.

## Installed background-removal models
1. General images/objects: U2NETP from rembg's official release.
   - E:/Video/models/u2netp/u2netp.onnx
   - 4,574,861 bytes; upstream MD5 verified: 8e83ca70e441ab06c318d82300c84806.
   - SHA256: 309c8469258dda742793dce0ebea8e6dd393174f89934733ecc8b14c76f4ddd8.
   - Rem bg preprocessing adapted under MIT; U-2-Net architecture/license notice retained.
2. People video: Robust Video Matting MobileNetV3 FP32 ONNX, official v1.0.0.
   - E:/Video/models/rvm/rvm_mobilenetv3_fp32.onnx
   - 14,975,696 bytes.
   - Installation SHA256: 88d4531297118f595bf2fd60f6f566aec2e559393802d1f436c380f0cbbd2828.
   - Recurrent states persist across frames; foreground and alpha are predicted.
   - GPL-3.0 license retained in tools/background-removal.

Both use the existing ONNX Runtime, NumPy, Pillow and FFmpeg. No Torch, OpenCV, SciPy, background server or full rembg package was installed.
Default video route is RVM for people. For arbitrary objects choose --model u2netp. RVM is not identity tracking; multiple people may be retained. Split scene cuts into separate commands so recurrent state resets.
Video processing streams decoded frames through memory instead of saving a large PNG sequence. Default output is 30fps CFR with maximum side 1280; change these options deliberately. Normalize HDR separately.

```powershell
. E:\Video\scripts\env.ps1
# Transparent image
& E:\Video\.venv\Scripts\python.exe E:\Video\scripts\remove-background.py image --input INPUT.jpg --output E:\Video\projects\my-reel\assets\processed\cutout-v1.png

# Two-second people preview
& E:\Video\.venv\Scripts\python.exe E:\Video\scripts\remove-background.py video --input INPUT.mp4 --output E:\Video\projects\my-reel\assets\processed\preview-v1.mp4 --mode composite --seconds 2 --max-side 640

# People video with transparency
& E:\Video\.venv\Scripts\python.exe E:\Video\scripts\remove-background.py video --input INPUT.mp4 --output E:\Video\projects\my-reel\assets\processed\person-v1.webm --mode alpha

# General object video matte
& E:\Video\.venv\Scripts\python.exe E:\Video\scripts\remove-background.py video --input INPUT.mp4 --output E:\Video\projects\my-reel\assets\processed\object-matte-v1.mkv --mode mask --model u2netp
```
INPUT paths are placeholders. Use fresh output filenames. Output companion QA JSON records settings and technical evidence; it is not a visual approval.

## Existing Gemini remover
Version 1.0.46, source https://github.com/GargantuaX/gemini-watermark-remover.
Wrapper: E:/Video/scripts/Remove-GeminiWatermark.ps1.
Uses the local D: CLI and existing E: headless Chrome through an E: preload adapter; no browser download or D: source change.
```powershell
& E:\Video\scripts\Remove-GeminiWatermark.ps1 -InputFile INPUT.png -OutputFile E:\Video\projects\my-reel\assets\processed\clean-v1.png
```
MP4 input/output also works. Preserve provenance and originals. The tool targets supported visible Gemini marks, not every watermark or invisible SynthID.
Actual image/video review is mandatory: one dark-background fixture retained a large star despite clean metadata. Do not silently accept that result or promise universal removal.

## Verification performed
- All 25 Claude skill entry files have valid YAML metadata.
- Context initialization, checkpoint copying, summary saving, session-start output and status line were exercised with sample input.
- Existing-output refusal and out-of-project path refusal passed.
- Native Claude auth status recognized the E: profile; Concat MCP remained Connected.
- U2NETP produced an alpha PNG, replacement-background MP4, alpha WebM and FFV1 matte.
- RVM produced person-isolated composite and alpha video, with recurrent state and test audio retained.
- Test video outputs decoded fully; expected six frames retained. Transparency verified by independent libvpx-vp9 decode, not a player screenshot.
- Gemini: standard image corner and short video watermark reviewed before/after; marks removed in sampled results. Separate difficult image fixture failed visual inspection despite clean metadata.
- Sampled stills inspected on opaque backgrounds. No continuous subjective audiovisual review, fine-hair motion trial, HDR trial, long video performance benchmark or paid Claude inference was completed.

Evidence: logs/extensions-20261024/verification.json and work/extensions-qa.
The tests prove local integration on short fixtures; evaluate masks and watermark processing on each real asset.

## Primary sources
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/statusline
- https://code.claude.com/docs/en/env-vars
- https://github.com/smixs/visual-skills
- https://github.com/danielgatis/rembg
- https://github.com/PeterL1n/RobustVideoMatting
- https://github.com/PeterL1n/RobustVideoMatting/blob/master/documentation/inference.md
- https://github.com/GargantuaX/gemini-watermark-remover

## 2026-10-25 render integration

All 25 direct Claude entry guides now route applicable video work through the current render contract, including local Windows/publish adaptations. CPU RVM remains the measured matting default; the separate CuPy colour and NVENC delivery paths do not imply GPU matting. Skills remain small; compiled GPU runtime dependencies are separate E: targets. /video-render-fast and the context render handoff connect the existing asset-generation/removal tools to the current edit without reprocessing unrelated stages.
