# Claude render integration update

Completed 2026-10-25 for VJ's E:/Video studio. **61 active instruction/code/configuration-bundle files synchronised**, including all 25 Claude skill entry guides and all 6 slash commands. No additional package, model or editor installation was needed.

## What changed

- Root CLAUDE.md, README and CLAUDE-CODE-GUIDE now route to one current render contract and a stage-specific file map. Old automatic AGENTS.md imports and the obsolete skills-junction description were removed from active guides.
- The director plan now connects content/audience/story/colour/motion/sound decisions to measured route selection, explicit output settings, stage timing, cache identity and exact-file QA.
- The render guide now includes every installed tool's role/limits, exact master/PNG/graphics/colour/audio/archive/concat recipes, revision invalidation and the required project handoff. Its section links support selective reading rather than loading everything into context.
- All 25 Claude skill entry guides apply those rules before upstream examples. Windows and publishing have direct local adaptations, replacing the old revoked-file reference and slow automatic social-export recipe. Original protected upstream sources/runtimes remain available as references; their old defaults do not govern the active Claude workflow.
- All 6 command routes share the contract, including direct rendering, Concat and simple editing. Tool choice depends on the current footage, requested route and verified capabilities.
- Project initialization now creates .context/RENDER.md and schema-2 render policy pointers. Checkpoints include the handoff. `init --no-activate` supports an independent job without switching the active project. Status and the existing SessionStart hook expose the current render contract.
- Style/feedback files retain their dated history but explicitly separate prior-video choices from current preferences. A new recording never inherits an old exposure value, warmth, face box, LUT or caption treatment by default.
- The current IMG_2442 project has a narrow RENDERING.md / RENDER.md handoff. Its existing creative state/manifest values and active-project pointer were preserved. The v11 benchmark grade does not implement the different ongoing v12 look, and an already-running pipeline was not retargeted.
- `master.py` now delegates to the current exporter. `Render-Test.ps1` is a fresh native synthetic pattern/tone encoder test, avoiding the old broken browser/AAC entry. The doctor reports current tool paths and limitations at logs/studio-doctor/latest.json without overwriting the old installation report.
- The small setup ZIP is refreshed with current instructions/helpers/skill guides. It remains a configuration/evidence snapshot for an existing studio, not a full runtime installer or permission to overwrite active project state.

## How Claude should work from now on

1. Resolve the actual requested project/source and read its state. For a NEW video inspect the content, audio, movement and metadata, then plan audience/story/takes/colour/motion/sound from that source. For SAME-PROJECT work retain that edit's approved treatment.
2. Record a concrete .context/RENDER.md: source and cut revision, grade/masks/temporal state, selected tools/profile, cache identities, approved master/mix, expected frames/duration, output path and pending checks.
3. Prefer native frame-accurate footage and format-validated Concat where suitable; reserve browser graphics for compositions with verified timing/pixels. The known OffthreadVideo and HTML5 footage failures remain real limitations.
4. Use explicit compatible CuPy colour only after current-job module/settings/parity checks. Keep measured CPU RVM matting unless a new configuration wins a valid test. Reuse one frame buffer; do not lower quality or switch a prior look to claim speed.
5. Recompute only affected stages. Matching current-job grade caches survive caption changes; audio-only changes copy compatible picture. Changed cuts invalidate timing-dependent cues. New footage gets fresh decisions.
6. Make one deliberate upload encode from the approved SDR 1080x1920 30 fps master or verified PNG cache with Export-Instagram.ps1, default NVENC `balanced` (updated 2026-10-25: tuned CQ24, ~89 MB per 80 s; the old `high` preset was retired). Colour + cuts now default to scripts/render-timeline-colour.py (plans/TIMELINE-RENDERER-v1.md). Record any explicit CPU fallback. Existing already approved deliveries may be reused. Avoid remastering approved AAC twice.
7. Preserve originals/masters. A smaller H.264 MP4 is lossy; FFV1 archival is a separate larger decoded-video-frame-lossless option. Never promise identical Instagram recompression or label VMAF a retained-quality percentage.
8. Check the exact export: metadata, frame count/duration, decode, source mapping/seams, captions/colour/masks, audio/sync and actual playback/listening coverage. Save stage times/output identity and only claim what was checked.

Use `/video-director` for the full content-led edit and `/video-render-fast` for the next explicit render. Read `CLAUDE-FILE-MAP.md` to find only the required stage.

## Validation actually completed

- YAML/name/description and render-policy links passed for all 25 skill guides and all 6 commands.
- Python and PowerShell syntax checks passed for changed executable entry points and the supported exporter wrapper.
- Isolated project initialization made RENDER.md without changing the active pointer; a repeated init preserved notes, and a checkpoint copied the handoff byte-for-byte.
- SessionStart returned the new workflow/fresh-source reminder; all 3 existing configured context hooks still reference the updated script.
- The legacy master entry's help exposes the real current exporter options.
- The doctor found the exporter, GPU colour target, regular Chrome, compatible binaries, source models and native Concat; it explicitly labels these as presence checks, not creative QA.
- The new synthetic smoke route produced 150 frames / 5 seconds at 1080x1920, 30 fps through NVENC and passed full decode. Delivery export took 5.307 seconds on this run. A pattern/tone test does not certify human masks, a new grade or browser video timing.
- All 25 skill changes were saved in the local Claude skills Git repository: `7cad58af2e2b9bfdbfa6793c621c72dda7328bb5`. That repository has no remote configured; this is a local installed-skill commit, not a cloud skill publication.

The earlier 9-second encoder and 12-frame colour benchmarks remain dated evidence in RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md; this documentation update is not another end-to-end creative render.

## Files updated

| File | Action |
|---|---|
| `.claude/commands/concat-edit.md` | Updated |
| `.claude/commands/free247editor.md` | Updated |
| `.claude/commands/video-director.md` | Updated |
| `.claude/commands/video-edit-simple.md` | Updated |
| `.claude/commands/video-render-fast.md` | Updated |
| `.claude/commands/video-studio-check.md` | Updated |
| `.claude/skills/broll/SKILL.md` | Updated |
| `.claude/skills/clips/SKILL.md` | Updated |
| `.claude/skills/codex-images/SKILL.md` | Updated |
| `.claude/skills/editing/SKILL.md` | Updated |
| `.claude/skills/gemini-clean-assets/SKILL.md` | Updated |
| `.claude/skills/hyperframes-animation/SKILL.md` | Updated |
| `.claude/skills/hyperframes-cli/SKILL.md` | Updated |
| `.claude/skills/hyperframes-core/SKILL.md` | Updated |
| `.claude/skills/hyperframes/SKILL.md` | Updated |
| `.claude/skills/image/SKILL.md` | Updated |
| `.claude/skills/insta-audit/SKILL.md` | Updated |
| `.claude/skills/outliers/SKILL.md` | Updated |
| `.claude/skills/publish/SKILL.md` | Updated |
| `.claude/skills/remove-background/SKILL.md` | Updated |
| `.claude/skills/request-video-assets/SKILL.md` | Updated |
| `.claude/skills/short-editing/SKILL.md` | Updated |
| `.claude/skills/short-translate/SKILL.md` | Updated |
| `.claude/skills/steal/SKILL.md` | Updated |
| `.claude/skills/studio-context/SKILL.md` | Updated |
| `.claude/skills/studio-script/SKILL.md` | Updated |
| `.claude/skills/studio-setup/SKILL.md` | Updated |
| `.claude/skills/video-edit/SKILL.md` | Updated |
| `.claude/skills/video-editor-windows/SKILL.md` | Updated |
| `.claude/skills/video/SKILL.md` | Updated |
| `.claude/skills/vox/SKILL.md` | Updated |
| `.context/INDEX.md` | Updated |
| `CLAUDE-CODE-GUIDE.md` | Updated |
| `CLAUDE.md` | Updated |
| `README.md` | Updated |
| `my-style/feedback.md` | Updated |
| `my-style/style.md` | Updated |
| `plans/CLAUDE-STORAGE-AND-CONTEXT.md` | Updated |
| `plans/CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md` | Updated |
| `plans/DIRECTOR-STUDIO-QUICK-START.md` | Updated |
| `plans/FAST-RENDER-WORKFLOW-v1.md` | Updated |
| `plans/GENERATED-ASSET-WORKFLOW.md` | Updated |
| `plans/RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md` | Updated |
| `plans/STUDIO-EXTENSIONS-SETUP-v1.md` | Updated |
| `plans/STUDIO-RUNTIME-REFERENCE.md` | Updated |
| `plans/VIDEO-STUDIO-INSTALL-PLAN-v1.md` | Updated |
| `plans/VIDEO-STUDIO-INSTALLATION-RESULT-v1.md` | Updated |
| `projects/img2442-motion-v1/.context/STATE.md` | Updated |
| `projects/img2442-motion-v1/.context/manifest.json` | Updated |
| `projects/img2442-motion-v1/README.md` | Updated |
| `research/claude-video-editing-2026-10-23/Claude-Video-Editing-Research-v1.md` | Updated |
| `scripts/Check-DirectorStudio.ps1` | Updated |
| `scripts/Render-Test.ps1` | Updated |
| `scripts/claude-context-hook.py` | Updated |
| `scripts/master.py` | Updated |
| `scripts/project-context.py` | Updated |
| `plans/CLAUDE-FILE-MAP.md` | Created |
| `projects/img2442-motion-v1/RENDERING.md` | Created |
| `projects/img2442-motion-v1/.context/RENDER.md` | Created |
| `plans/CLAUDE-RENDER-INTEGRATION-UPDATE-v1.md` | Created |
| `plans/Video-Studio-Setup-v1.zip` | Refreshed configuration bundle |

## Evidence and backups

Before/after file hashes and integration checks: `E:/Video/work/claude-render-sync-20261025/changes.json` and `validation.json`. Original instructions and the previous setup ZIP are backed up under that folder's `before/`. Existing media, old render receipts, the revoked root file and protected upstream sources were retained. Use the current active guides rather than restoring old default settings from those records.
