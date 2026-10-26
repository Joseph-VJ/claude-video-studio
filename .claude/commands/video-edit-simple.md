---
description: Edit local footage through free247editor and the installed pinned Herk engine.
argument-hint: <footage path and desired result>
---
Use /studio-context first. Read only the director-plan sections for the current stage, then E:/Video/repos/free247editor/.agents/skills/free247editor/SKILL.md and the appropriate kit/.claude/skills entry point. The system is already installed; use scripts/Check-DirectorStudio.ps1 to diagnose instead of reinstalling it.

Request: $ARGUMENTS

Load E:/Video/scripts/env.ps1 for every process. Use repos/free247editor/tools/transcribe.mjs with --local and a suitable installed model. Shared models and the canonical style/feedback paths are configured. For short videos use kit short-form-edit and its plan/footage validators. Keep one cut map, one colour pipeline and one caption track. Use root raw/ or a specifically supplied file; do not pick an unrelated old source. Put render internals in the project and a versioned final in out/ or the wrapper outbox/.

Missing image/video assets: use /request-video-assets, show manual generation prompts, track pending files, preserve originals, and inspect returned/processed assets. Use /gemini-clean-assets and /remove-background when relevant. Save the project context after each stage.

Design: before building text, captions, cards, icons, backgrounds or inserts use /video-design. Keep the project's .context/DESIGN.md current and audit rendered frames with its design-audit.py; avoid AI-default looks (neon, glow, stripe gradients, glass cards, emoji clip-art, rainbow accents, bounce on everything).

<!-- studio-render-integration:v1 -->
For applicable video work use E:/Video/plans/CLAUDE-FILE-MAP.md and the current stage of E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Keep the current project's .context/RENDER.md. Derive fresh creative settings/masks for new footage; same-project caches require matching identity. Native footage, verified graphics, one deliberate delivery encode and exact-file QA govern older upstream recipes.
<!-- /studio-render-integration:v1 -->
