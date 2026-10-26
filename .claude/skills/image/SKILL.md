---
name: image
description: "Write or improve copy-ready image-generation prompts for manually generated video assets, storyboards and reference images."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->
<!-- studio-design-contract:v1 -->
On-screen design (text, captions, cards, icons, backgrounds, motion, inserts) follows /video-design and the project's .context/DESIGN.md. Upstream looks and presets are vocabulary, not defaults. No neon, glow, stripe/indigo gradients, glass cards, emoji clip-art or rainbow accents unless the current brief asks; audit rendered frames with E:/Video/.claude/skills/video-design/scripts/design-audit.py.
<!-- /studio-design-contract:v1 -->

For video assets derive framing, palette and acceptance criteria from the current beat/colour plan, not the last recording. Generation remains manual and no provider call is implied.

Write prompts only; the user generates assets manually.
Use /request-video-assets for an edit's missing assets and tracking.
Confirm the user's generator/model if its syntax matters. If unspecified, provide a model-neutral prompt; do not invent supported model versions, quality tiers, durations or reference limits.
Describe subject, visible action, environment, composition, lighting, palette and intended timeline role. Give exact text only when essential; prefer adding titles in the editor.
For image edits separate Change, Preserve and Constraints. For subject extraction prefer a clear silhouette and a simple contrasting background; real transparency depends on the generator.
Return asset ID, recommended aspect ratio/resolution, input reference roles, one copy-ready prompt, expected filename, and concrete acceptance criteria.
Read only relevant reference sections: references/prompt-framework.md for complex composition; references/editing.md for edits; references/characters.md for continuity; references/storyboards.md for sequences; references/de-slop.md for natural photography.
Treat model-specific files as dated upstream advice; verify capabilities against the chosen provider's current official documentation before applying them.
Do not load all references. Do not call paid generation APIs or upload footage.
Reference library attribution: Serge Shima, smixs/visual-skills, CC BY 4.0. Local SKILL.md adapted for manual generation and selective context loading. See LICENSE and NOTICE.
