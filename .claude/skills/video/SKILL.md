---
name: video
description: "Write or improve copy-ready AI video-generation prompts for manually generated B-roll, inserts, keyframe animation and continuity."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->
<!-- studio-design-contract:v1 -->
On-screen design (text, captions, cards, icons, backgrounds, motion, inserts) follows /video-design and the project's .context/DESIGN.md. Upstream looks and presets are vocabulary, not defaults. No neon, glow, stripe/indigo gradients, glass cards, emoji clip-art or rainbow accents unless the current brief asks; audit rendered frames with E:/Video/.claude/skills/video-design/scripts/design-audit.py.
<!-- /studio-design-contract:v1 -->

For video assets use the current beat time, entry/exit handles and continuity/colour requirements. Generation remains manual. Re-check returned fps, duration, colour metadata and motion before it enters the timeline.

Write prompts; the user generates and returns clips manually.
Use /request-video-assets for missing assets in an editing project.
Build one achievable shot per generation: visible subject and action, start composition, camera movement with motivation, light, environment, progression and end frame. Separate subject movement from camera movement.
State duration, aspect ratio, intended output resolution, sound policy and exact editorial purpose. Include entry/exit handles, screen direction, recurring identity/wardrobe/palette anchors and reference image roles.
Fit the shot into an actual source-anchored beat, rather than adding unrelated spectacle. Do not fabricate documentary evidence.
If no generator/model is specified, write a model-neutral prompt and mark duration/resolution as requested targets. Check current official provider docs before emitting proprietary parameters. Do not assert that every tool accepts negative prompts, JSON, audio or keyframe control.
Return asset ID, timeline placement, one copy-ready prompt, continuity block, expected filename, and acceptance criteria.
Read only matching reference sections: references/dramaturgy.md for story; references/camera-lighting-vocabulary.md for camera/light; references/fixes-and-skeletons.md for continuity/failures; references/animatic-keyframes.md for storyboard inputs.
Treat model-specific reference files as dated advice requiring official verification.
Do not generate via APIs, spend credits, or upload source media.
Reference library attribution: Serge Shima, smixs/visual-skills, CC BY 4.0. Local SKILL.md adapted for manual generation and selective context loading. See LICENSE and NOTICE.
