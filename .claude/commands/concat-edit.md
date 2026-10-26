---

description: Use the installed Concat MCP engine for an editable local timeline and colour workflow.

argument-hint: <footage path and desired result>

---

Use /studio-context. Read relevant sections of the director plan and current style/feedback. Discover the concat server's tools and schemas before operations. Keep media/projects/exports under E:/Video. Do not edit an unrelated open project. Use explicit colourSpace when changing video settings; preserve unrelated fields and the entire existing effect chain when updating one effect. Save projects explicitly. Review composited frames and the exported file, not only API success responses. Verify colour, captions and audio on a synthetic example before promising an unsupported capability.



Request: $ARGUMENTS



Missing image/video assets: use /request-video-assets, show manual generation prompts, track pending files, preserve originals, and inspect returned/processed assets. Use /gemini-clean-assets and /remove-background when relevant. Save the project context after each stage.



Design: before building text, captions, cards, icons, backgrounds or inserts use /video-design. Keep the project's .context/DESIGN.md current and audit rendered frames with its design-audit.py; avoid AI-default looks (neon, glow, stripe gradients, glass cards, emoji clip-art, rainbow accents, bounce on everything).

<!-- studio-render-integration:v1 -->

For applicable video work use E:/Video/plans/CLAUDE-FILE-MAP.md and the current stage of E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Keep the current project's .context/RENDER.md. Derive fresh creative settings/masks for new footage; same-project caches require matching identity. Native footage, verified graphics, one deliberate delivery encode and exact-file QA govern older upstream recipes.

<!-- /studio-render-integration:v1 -->


Concat draws on the GTX1650 via DX12, but H.264 prefers CPU x264 in this version. The tested H.264/MP4 input scored well; the FFV1/MKV input had cadence issues. Validate the actual source format, effects and exact output. Do not automatically re-encode an approved Concat delivery just to force NVENC.
