---
name: request-video-assets
description: "Identify missing images or videos during an edit, write generation prompts for the user, track returned assets and resume editing."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->
<!-- studio-design-contract:v1 -->
On-screen design (text, captions, cards, icons, backgrounds, motion, inserts) follows /video-design and the project's .context/DESIGN.md. Upstream looks and presets are vocabulary, not defaults. No neon, glow, stripe/indigo gradients, glass cards, emoji clip-art or rainbow accents unless the current brief asks; audit rendered frames with E:/Video/.claude/skills/video-design/scripts/design-audit.py.
<!-- /studio-design-contract:v1 -->

Record incoming/processed asset hashes and tool/settings provenance. A changed asset invalidates only its dependent composite/export/QA, not unrelated source transcription or approved grades. Check the actual current edit handles and colour path before integration.

Inspect source content, audience and current beat plan first. Request an asset only if it helps explain a point, bridges a cut, or supplies a genuinely missing shot.
Initialize project context with /studio-context. For each asset create assets/requests/ASSET-ID.md and a row in .context/ASSET-REQUESTS.md.
Provide: asset ID; why needed; source/timeline anchor; image or video; intended duration and handles; aspect ratio/resolution; matching reference roles; continuity constraints; copy-ready prompt; avoid/fix criteria; exact expected filename; save location assets/incoming.
Use /image for stills and /video for clips. Never generate via a paid API: the user explicitly generates manually.
Show the prompt in chat as well as saving it. Mark status awaiting-user-generation. Continue independent editing using clearly labelled placeholders; do not call the final output complete while required assets are missing.
On return inspect dimensions, frame rate/duration, colour, subject continuity, hands/text, motion boundaries and audio. Record tool/model and rights/provenance. Preserve the original and make processed versions.
Use /gemini-clean-assets for supported visible Gemini watermarks. Prefer an official watermark-free export when available; do not imply it removes invisible provenance.
Use /remove-background when needed. Update the asset manifest, replace the correct placeholder, render and inspect the affected cut and full output as feasible.
