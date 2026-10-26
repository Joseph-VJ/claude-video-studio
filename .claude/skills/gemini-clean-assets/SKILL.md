---
name: gemini-clean-assets
description: "Process local Gemini-generated image or video assets with the existing D: Gemini watermark remover and inspect the result."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->

Keep source/processed versions and tool/settings identity. Inspect the cleaned pixels, including motion: clean metadata alone is not visual proof. Reprocess only changed assets; do not trigger an unrelated full grade.

Load E:/Video/scripts/env.ps1. Reuse D:/gemini-watermark-remover; do not run npm install or modify that checkout.
Use E:/Video/scripts/Remove-GeminiWatermark.ps1 -InputFile <local asset> -OutputFile <new E: file>.
The wrapper invokes node D:/gemini-watermark-remover/bin/gwr.mjs remove INPUT --output OUTPUT --json.
Process the user's generated assets or material they are authorized to modify. Preserve original files, generator information and provenance. This targets supported visible Gemini watermarks; it is not a universal remover and does not remove SynthID.
Inspect before/after corner crops and full frames for stars, dark holes, texture loss and banding. For video sample first/middle/last and moving-detail frames, then watch the affected area in motion where available. Do not equate a detector's clean score with independent visual proof.
If unsupported or damaged, retain original, report limitation and request an official clean export. Do not silently crop away content or repeatedly inpaint it.

Installation QA found a dark-background image fixture where a large star remained despite clean metadata. Treat clean metadata as insufficient; inspect actual before/after output and report failures. Standard images and a short video have separate smoke tests.
