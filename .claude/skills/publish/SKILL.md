---
name: publish
description: "Prepare the current approved video's delivery files and posting copy, and publish only when the user explicitly requests and authorizes that action."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->

# Delivery and publishing

Use the exact video/project named by the current request or its verified current-project handoff. Do not select an unrelated old recording, the latest file in a global output folder or a benchmark as the source. Confirm exact-file QA and unresolved issues before describing a kit as ready.

Read E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md for rendering and E:/Video/plans/CLAUDE-FILE-MAP.md for stage references. Preserve the approved master. Reuse a suitable already approved delivery when possible; otherwise encode once from the approved master using E:/Video/scripts/Export-Instagram.ps1 with Encoder nvenc / Quality balanced (default, ~89 MB per 80 s). Do not run the upstream slow-x264 social export recipe or re-encode just for a different output name.

A transport service's file-size cap is not an Instagram quality requirement. Verify the actual selected upload route's current limits before depending on them. The quality-first preset does not guarantee a fixed MB size. Never silently choose compact, reduce resolution/fps or squeeze bitrate to fit an old 30 MB assumption. If the selected transport cannot carry the quality-approved file, prepare a manual-upload kit or present the concrete tested trade-off. A smaller MP4 is lossy; FFV1 archival is separate.

Copy approved AAC audio rather than remastering it repeatedly. For audio-only changes preserve the compatible H.264 picture. Verify final dimensions/fps, metadata, decoded frames, seams, captions, sound and exact output identity. Keep cover/copy/source provenance in the current project; derive claims, names and numbers from the supplied content.

Preparing files does not authorize sending or publishing. Follow the user's explicit requested scope and any applicable posting workflow for the specified platform/account/video. No account connection, paid service, publication, scheduling or source-media upload is implied by rendering. The default asset-generation method remains manual prompts.

For a specifically authorized platform workflow, read only the relevant procedure from E:/Video/.agents/skills/publish/SKILL.md as dated upstream reference. Apply current studio/user rules first, verify changing platform/tool capabilities, and use Windows-compatible installed tools. Do not run Mac/Linux installers or inherit its automatic file selection, old size caps, slow encoder command or generic safe-zone assumptions.
