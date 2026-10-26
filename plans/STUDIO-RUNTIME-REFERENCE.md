# Director Video Studio

Current file index: CLAUDE-FILE-MAP.md. Operational render contract: FAST-RENDER-WORKFLOW-v1.md (including exact recipes, tool roles, cache invalidation and handoff). Historical test evidence must not be mistaken for current-project QA.

The earlier AGENTS.md instructions were explicitly revoked by VJ. Do not import or reinstate them. Use current user requests, the director plan and applicable higher-priority instructions.

For a new video request, read @plans/CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md before choosing cuts or a look. Understand the actual content, identify a primary audience with labelled assumptions, and write a concrete beat plan with source anchors. One agent may perform the director, editor, motion, colour, sound and verification roles sequentially. Psychology labels do not establish a retention result.

This installation uses E:/Video. Start commands by loading scripts/env.ps1 so tools, models and caches use the installed runtime. Python: E:/Video/.venv/Scripts/python.exe. Reuse installed tools and models before downloading anything.

## Editing routes
- /video-director: content/audience/story planning and the full selected workflow.
- /video-edit-simple: free247editor with pinned Herk engine at repos/free247editor/kit. Read the wrapper skill and relevant engine skills there. Use local transcription, not ElevenLabs or Groq by default.
- /concat-edit: the optional Concat MCP timeline/colour route. Discover tool schemas and preserve full settings/effect chains when changing one value.
- /video-studio-check: installed-runtime and connection diagnostics.

Read my-style/style.md and my-style/feedback.md before each edit. Preserve the difference between lasting preferences and project-specific choices. The existing speaker preferences favour a naturally visible face, warm natural skin and meaningful speech-timed graphics. Confirm language/caption treatment from the current brief; do not carry one project's no-text rule into every video.

Preserve original recordings and existing projects. Use versioned outputs. Keep an editable project, source-to-output timing, and QA tied to the exact output. Inspect actual rendered motion and colour; do not claim full audiovisual review from stills or a transcript alone. No publication, paid service or source-media upload is implicit in an editing request.

Existing tenfoldmarc/Melvyn skills remain available under .claude/skills. Their aesthetic defaults are examples; this plan and the user's current brief control the treatment. Use only one cut owner, caption track and main finishing path.

## Fast render and Remotion delivery paths
The bundled Remotion ffprobe crashes on this PC. The dedicated binaries directory at E:/Video/tools/remotion-native-4.0.537 uses the working system FFmpeg/ffprobe. That FFmpeg does not provide libfdk_aac, so do not use direct Remotion AAC encoding as the production path.

Use /video-render-fast and plans/FAST-RENDER-WORKFLOW-v1.md for measured route selection, quality limits and cache rules. scripts/Export-Instagram.ps1 exports an explicit 1080x1920 30 fps SDR master using H.264 NVENC with the `balanced` preset by default (p7 tuned CQ24, ~89 MB per 80 s; `max` = tuned CQ20 on request), or accepts an existing contiguous PNG directory with -Frames and separate mixed audio. A smaller MP4 is lossy; preserve the source/master. FFV1 archival mode is available separately.

For custom Remotion graphics, scripts/Render-DirectorProject.ps1 retains muted PNG frame capture and now sends those PNGs directly to the exporter for one video encode and audio mastering. It uses the installed regular Chrome by default and permits an explicit -BrowserExecutable override. The previous helper is saved alongside it. Run from projects/renderer. A 270-frame HTML5/H.264 PNG capture completed but its VMAF 93.25/mistimed frames failed the footage quality gate; prefer native footage plus separately verified graphics. OffthreadVideo with the FFV1 reference still crashed, and headless-shell startup timed out. Do not assume arbitrary compositor paths are fixed, or turn on shared-memory capture with substituted generic FFmpeg binaries. Concat native H.264/MP4 and the FFV1/MKV input have separate cadence/quality results in plans/RENDER-SPEED-RESEARCH-AND-RESULTS-v1.md.

Claude sign-in is still required in the dedicated E:/Video/cache/claude profile. Do not claim that a paid Claude inference or a real creative edit was tested during installation.