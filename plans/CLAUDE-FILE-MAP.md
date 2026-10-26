# Claude studio file map

Updated 2026-10-25 for the measured render optimisations; 2026-10-26 added the `/video-design` stage. This is the index, not an instruction to read every file each time.

## Start and precedence

1. Read `E:/Video/CLAUDE.md` and the current request.
2. Check `.context/active-project.txt`; read that project's `.context/STATE.md` and `.context/RENDER.md` when present. Confirm the source/project matches the request. Do not select the newest old output as a new video's source.
3. For a NEW recording, inspect its actual content, audio, motion and colour metadata; make a fresh content/audience/edit/colour/motion/sound plan. Previous grades, masks, white balance, LUTs and scene choices are not defaults. Continue an existing edit with its own explicitly approved treatment.
4. Read the section needed for the current stage. Keep long transcripts, logs and benchmark evidence in files; do not paste them into model context.

Current requests and applicable higher-priority instructions govern. The former root AGENTS.md was revoked; do not restore it from legacy skills or archives. The current render contract is `FAST-RENDER-WORKFLOW-v1.md`. Upstream examples, old project README commands and historical installation records do not replace that contract.

## Read only what this stage needs

| Stage | File or entry point | Read for |
|---|---|---|
| Brief, content, audience, director/editor roles | `CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md`, `/video-director` | Source-anchored story, viewer assumptions, performances, beats and role decisions |
| On-screen design: text, captions, cards, icons, backgrounds, motion, AI inserts | `/video-design` (`.claude/skills/video-design`), project `.context/DESIGN.md` | Design constitution from the footage, anti-AI-look rules, motion grammar, `design-audit.py` frame audit and checklist |
| Render choice and settings | `FAST-RENDER-WORKFLOW-v1.md`, `/video-render-fast` | Native/GPU routes, explicit grade adapter, cache, commands, quality and delivery |
| Default colour + cut render, smaller delivery | `TIMELINE-RENDERER-v1.md`, `scripts/render-timeline-colour.py` | Cut-first renderer config, measured speed (3.18 fps), parity method, `balanced` delivery measurements |
| Installed tool capabilities | `FAST-RENDER-WORKFLOW-v1.md` section 11, `STUDIO-RUNTIME-REFERENCE.md` | Exact helper/tool paths, when to use them and current limits |
| Why these paths were chosen | `RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md` | Measured tests and primary sources; open only the relevant test |
| Launching and first commands | `DIRECTOR-STUDIO-QUICK-START.md` | Studio launch, render commands and where output goes |
| Small context files and cache identities | `CLAUDE-STORAGE-AND-CONTEXT.md`, `/studio-context` | Fresh job versus same-project resume, checkpoints and safe cache reuse |
| Missing image/video assets | `GENERATED-ASSET-WORKFLOW.md`, `/request-video-assets`, `/image`, `/video` | Copy-ready prompts for manual generation, filenames, timing and acceptance checks |
| Returned assets | `/gemini-clean-assets`, `/remove-background` | Preserve provenance; validate visible-mark processing, alpha and temporal masks |
| Simple edit through installed kit | `/video-edit-simple`, `/free247editor` | Explicitly selected free247editor/Herk workflow, current render contract still applies |
| Native editable timeline | `/concat-edit` | Concat MCP schemas, retained project/effects, format-specific export checks |
| Runtime checks | `/video-studio-check`, `scripts/Check-DirectorStudio.ps1` | Installed files/versions and the distinction between presence and successful execution |
| Synthetic encoder smoke test | `scripts/Render-Test.ps1` | Generated test pattern/tone; no creative footage or browser correctness claim |
| Historical setup | `VIDEO-STUDIO-INSTALL-PLAN-v1.md`, `VIDEO-STUDIO-INSTALLATION-RESULT-v1.md`, `STUDIO-EXTENSIONS-SETUP-v1.md` | Dated installation evidence. Use current render guide for operations |

## The handoff Claude must maintain

Keep source IDs/hashes, the current brief, cut/timing revision, explicitly approved colour path/settings/masks, pending assets and selected tool in the project. Record stage timings, cache keys, source/dependency identity, exact command/output hash and what was actually checked. An instruction update is not a new video render or new QA receipt.

For the current IMG_2442 edit, read its own state and `RENDERING.md`; do not substitute the v11 benchmark grade for the ongoing v12 colour work. New footage never inherits that project's settings.

## Historical files and upstream engines

Original media, old rendered revisions, benchmark logs and `.pre-fast-render-20261025.ps1` are preserved. They document earlier behaviour; they are not the default future workflow. Original upstream `.agents` skill sources and pinned third-party engine repositories are reference/runtime sources. Claude's local entry guides apply this studio's Windows/E: and render rules before consulting those sources. Do not run upstream installers or choose a fixed house look just because an example does.
