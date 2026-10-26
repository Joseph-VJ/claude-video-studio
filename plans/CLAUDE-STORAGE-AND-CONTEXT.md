# Storage and context
Launch Start-DirectorStudio.cmd or Start-ClaudeVideo.ps1. Both set CLAUDE_CONFIG_DIR on E: before Claude starts.
Scope: this video studio and its child tools. Existing Windows/Claude executables stay where already installed.
This does not relocate Windows paging, operating-system files, other Claude launch methods, browser profiles, or third-party hardcoded paths.
Caches/models/temp are redirected using scripts/env.ps1. Do not set HOME or USERPROFILE globally.
Skills are small instructions; model weights and rendered frame sequences dominate storage.
Native Claude sessions remain in cache/claude; automatic memory uses .context/claude-memory.
Use project-context.py init --project E:/Video/projects/NAME to initialize a project.
Update STATE.md after each completed stage: actual source anchors, cut decisions, pending assets, exact output and checks, next action.
Use /context to inspect token usage and /cost for usage where supported. Use /compact after a checkpoint for the same edit; /clear for a different task.
No skill can enlarge the model context window or guarantee token savings. Files only save context when Claude selectively reads them.
PreCompact copies small current notes, not the full media/transcript. PostCompact stores only the latest summary in the project.
Review cache sizes before large renders; estimate raw frames = width * height * channels * frame count (PNG compression varies).
Do not delete source media, models, projects, credentials or active render folders as cache cleanup.
Record cleanup candidates in the project and delete only proven rebuildable files within an explicitly selected cache folder.
Use existing local tools before any new package/model. New software stays on E:; keep the D: Gemini checkout read-only.

## Render context and same-job cache reuse

Read plans/CLAUDE-FILE-MAP.md and the needed section of FAST-RENDER-WORKFLOW-v1.md. Keep .context/RENDER.md alongside STATE.md; checkpoints include it. Record current source hash/ranges, cut/grade/mask revisions, selected engine/encoder, runtime/model identities, cache keys, stage times, exact output and pending QA. New init templates include these pointers; existing decisions are not overwritten.

A NEW recording gets new analysis, interpretation, grade and masks. The active pointer does not authorize reusing another video. For a SAME-PROJECT revision, retain only stages with matching identities. Caption changes retain a valid grade; audio-only revisions copy approved video; changed cuts invalidate dependent cues. Never adopt the v11 benchmark settings for the different v12 grade or a new recording.

Use `project-context.py init --project E:/Video/projects/NAME --no-activate` to prepare an independent job without switching the active pointer. Activate deliberately only when it is the requested current job. A SessionStart/compact hook reminds and copies notes; it does not select settings, run a render or infer editorial decisions.

Approximate new isolated GPU runtime footprint from the research is 877.5 MiB plus caches/downloads on E:. Model/frame caches can be much larger. Check free space before FFV1/PNG sequences; never remove approved masters, active workers or source recordings to meet a speculative space target. No additional package is needed for this instruction update.
