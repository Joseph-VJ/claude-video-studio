---
description: Check installed video studio tools, pinned repos, local models and optional Concat MCP.
---
Run E:/Video/scripts/Check-DirectorStudio.ps1 from PowerShell. Read its saved JSON report and report actual passes, failures and missing capabilities. Do not start a real edit or reinstall working dependencies as part of diagnostics.

<!-- studio-render-integration:v1 -->
For applicable video work use E:/Video/plans/CLAUDE-FILE-MAP.md and the current stage of E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Keep the current project's .context/RENDER.md. Derive fresh creative settings/masks for new footage; same-project caches require matching identity. Native footage, verified graphics, one deliberate delivery encode and exact-file QA govern older upstream recipes.
<!-- /studio-render-integration:v1 -->

Read the current report at E:/Video/logs/studio-doctor/latest.json. Distinguish files/encoder presence from device execution, sample success and creative QA. Optional synthetic encoder testing is scripts/Render-Test.ps1; it does not certify browser footage paths.
