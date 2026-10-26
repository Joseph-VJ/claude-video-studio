# Use this video studio in Claude Code

1. Launch E:/Video/Start-DirectorStudio.cmd, or run `& 'E:\Video\Start-ClaudeVideo.ps1'` in PowerShell. Use your existing account if sign-in is requested. The launcher keeps studio state/caches on E:.
2. For a new recording give its exact path, audience/goal and constraints, for example: `/video-director Edit E:/Video/raw/NEW-recording.mp4 into a clear Instagram Reel. Inspect its full content and actual metadata, make a fresh audience/story/colour/motion/sound plan, then create a versioned draft.` Do not choose an old output or the last recording by default.
3. For rendering use `/video-render-fast [current project or approved master, new output name]`. Read plans/FAST-RENDER-WORKFLOW-v1.md for exact supported commands, GPU/CPU choices, cache rules and quality checks. plans/CLAUDE-FILE-MAP.md locates the needed stage without loading all guides.
4. To continue the existing edit, explicitly name E:/Video/projects/img2442-motion-v1 and your feedback. Read its STATE.md, RENDER.md and RENDERING.md. Keep its current v12 creative decisions; the v11 benchmark is not the v12 grade. Record what changes, reuse only valid stage caches, render a new version and attach new QA to that exact file.

## What Claude now knows

- The 26 Claude skill entry folders (including the new /video-design) are direct files under .claude/skills, including small forwarding guides for original E: runtimes. It is no longer the old skills junction. /video-director, /video-render-fast, /video-edit-simple, /free247editor, /concat-edit and /video-studio-check share the current studio rules.
- New footage needs fresh content, colour/masks and creative planning. Lasting preferences and old project examples cannot automatically supply a previous grade or face box.
- The cut-first timeline renderer (default colour + cut route), NVENC `balanced` delivery (~89 MB per 80 s), explicit compatible CuPy colour, the fixed pipe reader, CPU RVM, native footage and verified custom graphics are distinct tools/stages. Presence is not proof of execution or quality.
- Export an approved master/PNG cache only once for upload. For audio-only changes copy compatible picture. Small MP4 is lossy; keep the master and separate true-lossless archival.
- Existing browser footage paths have crash/timing limitations. Never claim they are repaired or a new creative output passed simply because a synthetic test completed.
- SessionStart points to the current handoff; checkpoints include RENDER.md. Saving notes does not make editorial decisions automatically.
- On-screen design goes through `/video-design` first: a per-project DESIGN.md built from the footage and an audit of rendered frames, so text, cards, icons and motion do not fall back to AI-default looks (neon, glow, stripe gradients, emoji clip-art, rainbow accents).
- Missing assets use copy-ready prompts for manual generation. No paid service, publication or source-media upload is implied.

For a simple editing route choose /video-edit-simple. For a native Concat timeline choose /concat-edit. Legacy /video-edit and /editing remain available but their local entry guides apply the current studio contract before upstream examples. No new installation is needed to use this update.
