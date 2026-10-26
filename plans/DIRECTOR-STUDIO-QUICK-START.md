# Director Studio — Quick Start

## Start Claude

Double-click E:/Video/Start-DirectorStudio.cmd in File Explorer, or run this in PowerShell:

    & 'E:\Video\Start-DirectorStudio.ps1'

Sign in once when Claude asks. The dedicated studio profile was not signed in during installation. Use an eligible Claude account/plan or your chosen supported authentication; no model subscription was purchased or credential copied by this setup.

## Make an edit

Put a recording in E:/Video/raw, then give Claude an exact path and the intended audience/result. For example:

    /video-director Edit E:/Video/raw/my-video.mp4 into a clear Reel. Understand the message, identify the audience, plan the story, protect natural skin colour, add useful speech-timed graphics, and make a draft.

Other commands:

- /video-director PLAN ONLY [file and brief]
- /video-edit-simple [file and brief]
- /free247editor [file and brief]
- /concat-edit [file and brief]
- /video-render-fast [current project or approved master and output]
- /video-studio-check

Use plans/CLAUDE-FILE-MAP.md to read only the needed stage. The director plan is referenced by E:/Video/CLAUDE.md and loaded selectively. Every new recording needs fresh colour, masks and content decisions; old projects/lab jobs are not presets. The canonical style and feedback remain E:/Video/my-style/style.md and feedback.md. Tell Claude which instructions apply to one video versus every future edit.

## Optional timeline app

Double-click E:/Video/Start-Concat.cmd to open Concat. Its native MCP server is registered with Claude Code for E:/Video, and its headless workspace is limited to E:/Video. Close an agent-owned project before opening that same project in the GUI. Live editing of the visible open timeline is not promised by this installed release.

## Custom Remotion graphics

Use /video-render-fast and plans/FAST-RENDER-WORKFLOW-v1.md. Export an explicit approved 1080x1920 30 fps SDR master with scripts/Export-Instagram.ps1 (default Quality balanced: NVENC p7 tuned CQ24, ~89 MB per 80 s). Colour + cuts for a new video render through scripts/render-timeline-colour.py (cut-first, see plans/TIMELINE-RENDERER-v1.md). You can also feed an existing verified PNG sequence with -Frames and separate mixed audio. Render-DirectorProject.ps1 captures graphics PNGs and sends them directly to that exporter, without an intermediate H.264 encode.

Native FFmpeg and format-validated Concat are preferred for ordinary footage. Remotion OffthreadVideo and HTML5 footage paths have unresolved crash/frame-timing issues; installed regular Chrome does not repair them. Use custom graphics only after their actual composition passes QA. Keep the master; small upload MP4 is lossy and FFV1 archival is separate. See the guide for every flag, CPU fallback and audio-only picture-copy changes.

## Scope of the checks

The original installation tests used synthetic speech, graphics and colour patches. The 2026-10-25 render research also tested real-footage stage samples and exported an existing v11 master; it did not certify a complete new edit, the current v12 grade, or full moving playback/listening. See plans/RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md. A real edit still requires reviewing your actual content, take choices, skin tone, HDR interpretation, moving masks and preferred visual style. No finished video was published or source recording uploaded.
