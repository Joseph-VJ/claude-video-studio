# Feedback history and scope

Read only feedback relevant to the named current project/version. These dated records preserve prior decisions; they are not default settings for a new recording or permission to delete current files. For a new video start fresh; for an existing video follow its latest explicit brief/state and record scoped revisions.

Render methods and terminology are superseded by plans/FAST-RENDER-WORKFLOW-v1.md. ProRes 4444 and H.264, including CRF10, are lossy; historic phrases such as lossless-quality describe an intended appearance, not decoded-frame identity. Preserve masters and use FFV1/hash checks for a true video-frame lossless archive. Keep new output QA tied to that exact version.

## Earlier project feedback

2026-10-26 — VJ: "when the AI is editing it looks like clear AI design" — asked for a design skill that avoids the AI/neon look; also said "I love the 2 videos, fresh v1 and v12". Added /video-design (.claude/skills/video-design). Its audit of fresh-v1 found a full-screen electric-blue wipe (#2457FF) at 16 s, more than 4 accent hues in ~45% of frames, 8 hue families, 10+ shadow styles and stripe gradients; v12 had glossy 3D emoji icons, generic avatars and pastel blobs. These are craft fixes inside the approved structure, not a request to redo either video.


2026-10-21 — IMG_2442.MOV: Understand the spoken content; add relevant motion graphics and colour correction; make the underexposed face clearly visible while preserving natural skin tone.

2026-10-21 — Confirmed caption preference: same language as the speaker (Tamil).

2026-10-22 — IMG_2442.MOV v2: edit in an Alex Hormozi (@hormozi) style for Instagram Reels. Use NO text at all (no captions, no words or numerals in graphics); do everything else (fast punch-zoom cuts, sound design, colour) and use motion graphics. Rendered as IMG_2442-edited-v2-hormozi; v1 (Tamil captions) is kept unchanged.

2026-10-22 — IMG_2442 v3: colour correction was "too wrong" in v2 (face too dark/orange against a blown-out wall). Regraded from the original HLG source with a proper film-style grade: Hable tone-map base, feathered face window (exposure-style lift without raising blacks, warm natural skin, calmer shine), gentle film curve with warm highlight roll-off, no vignette (it darkened the graphics area). Rendered as IMG_2442-edited-v3-hormozi. Old v1/v2 edited videos deleted at the user's request.

2026-10-22 — IMG_2442 v4: user said v3 colour was still wrong, asked to reset and redo, and to actually look at the video. Findings from full-resolution frames: v3 face was ashen/chalky (cheeks 61-81% luma, ~20% saturation, same tone as wall) because gamma-space curve lifts desaturate skin. Rebuilt from scratch: linear-light exposure (+0.8 stop) in a soft face window, faded out on bright pixels (no halo), Hable shoulder, gentle warm balance, mild film curve. Output IMG_2442-edited-v4-hormozi.mp4. Pipeline colour drift checked: none (wall/shirt within 1-2 levels). Memory folder was empty and no colour defaults exist in code.

2026-10-22 — IMG_2442 v5: (1) too many files per version: build intermediates now render to projects/img2442-motion-v1/work/render/ and only the mastered final goes in out/; superseded versions are deleted. (2) Reference videos in E:/Video/video referecne (podcast before/after reels): cinematic warm grade, tight punch-ins, full-screen insert cards on a soft light backdrop with tilted poster cards and pastel pills, colour washes, notes/poster collages, split screen (image on top, speaker below), kinetic text. Rebuilt the whole edit in that language with ~55% full-screen motion-graphic scenes and ~25% split-screen, using drawn graphics only. Reference text style was NOT copied because the user's standing instruction is no text. (3) Face still slightly too light in v4: regraded at +0.5 stop with a gentle mid-tone deepening.

2026-10-22 — IMG_2442 v7: user asked for (1) text: understand the Tamil and use the most important words in English; (2) colour grade improved only a little (they liked v5); (3) lossless video output. Done: kinetic English keywords timed to the spoken Tamil words (Anton caps + Meie Script accents, red bar for problem words, green/yellow for positive), subtle grade polish (mild S-curve, +4% saturation, warmer face highlights, less lilac shine), and a lossless-quality pipeline (PNG frames -> ProRes 4444 master -> one visually-lossless H.264 CRF 10 encode, AAC 320k). Reference text style was adopted this time because the user lifted the no-text rule.
