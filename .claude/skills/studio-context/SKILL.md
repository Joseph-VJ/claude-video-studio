---
name: studio-context
description: "Initialize, checkpoint or resume a video editing project using small local context files on E:, and inspect token or disk usage."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->

Maintain .context/RENDER.md with current source/cut/grade identity, stage choices/times, cache keys, exact output and pending QA. Checkpoints now include it. init --no-activate prepares an independent project without changing the active pointer. Reuse only matching same-job stage caches; new footage gets fresh decisions.

Load E:/Video/scripts/env.ps1. Use E:/Video/.venv/Scripts/python.exe.
Initialize: scripts/project-context.py init --project E:/Video/projects/NAME
Resume: scripts/project-context.py status
Checkpoint: scripts/project-context.py checkpoint
Disk: scripts/project-context.py disk
Read the project's .context/STATE.md first; confirm the active project matches the user's request. Load only relevant manifest entries, transcript ranges, plan sections and style notes.
Update STATE.md at each stage with goal, source anchors, chosen timeline owner, latest exact output, checks actually passed, pending assets and next action. Keep it below 80 lines. Put reasons in DECISIONS.md and asset requests in ASSET-REQUESTS.md.
Before /compact, save a checkpoint and a concise handoff. /context measures live context; /cost shows available usage. /clear starts another task; do not clear before saving unfinished work.
Native hooks copy existing notes before compaction; they do not infer editorial decisions. Never promise automatic context recovery without maintained notes.
Use file paths instead of repeated full logs, large JSON, transcripts, base64 or all skill guides. Prefer targeted search and line ranges. No new agent is needed for routine stages.
Never remove originals, models, credentials or active caches. Identify large rebuildable caches and their owner before cleanup.
