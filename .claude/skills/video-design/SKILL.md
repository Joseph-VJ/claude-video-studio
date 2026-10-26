---
name: video-design
description: "Design the on-screen layer of a video (text, captions, cards, colour of graphics, icons, backgrounds, motion, AI inserts) so it looks crafted by a human designer and not like a generic AI template: no neon, glow, stripe gradients, glossy emoji clip-art or rainbow accents. Use before building any graphics, captions or inserts, when reviewing a draft's look, or when the user says it looks AI, cheap, template, neon, too much, or asks for better design."
---
<!-- studio-render-contract:v1 -->
For this E: video studio, follow E:/Video/CLAUDE.md and the relevant stage in E:/Video/plans/CLAUDE-FILE-MAP.md. Before rendering or changing a render plan, use E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md. Current job decisions and the tested local paths govern older upstream examples. Never restore the revoked root AGENTS.md, assume an old look/mask applies to new footage, reinstall working tools, or treat a small MP4 as mathematically lossless. Keep technical delivery settings separate from fresh creative settings.
<!-- /studio-render-contract:v1 -->

# Video design: crafted, not AI-default

The on-screen design layer is one role in the director plan (motion designer and caption editor, Pass D/E). This skill is how that role makes decisions. It does not own the cut, the grade or the render; it owns what is drawn on top of the footage and how it moves.

Why it exists: when no one makes a design decision, the model falls back to the most common patterns in its training data (default font, purple/blue gradients, glass cards, glow, emoji icons, a different accent for every word). Viewers have seen those patterns thousands of times, so the video reads as "made by AI" before a word is understood. The fix is not "less design"; it is design that was chosen for this speaker, this footage and this message, then held consistently.

## What VJ has approved (2026-10-26)

VJ said they love IMG_2442-fresh-v1 and IMG_2442-edited-v12. Treat their **structure and energy** as approved: big English keywords and rupee numbers tied to the Tamil speech, two-person comparisons, split speaker/insert windows, AI inserts in windows, a clear call-to-action, motion inside every beat. This skill **refines the craft inside that structure**; it does not replace it with a quiet minimal look. Do not change an approved edit's design unless the current brief asks for it. For new videos, start from these strengths and avoid the tells listed in [references/anti-ai-tells.md](references/anti-ai-tells.md), several of which appeared in those drafts.

## Workflow

Read only the reference file for the step you are on.

1. **Inputs.** Read the current brief, my-style/style.md and my-style/feedback.md (design-relevant lines), the project's beat plan and transcript ranges. For a SAME-PROJECT revision read its `.context/DESIGN.md` and keep it unless the user asks for a change. A NEW video gets a new design constitution; the previous video's palette, fonts or icon set are not defaults (lasting preferences above still apply).
2. **Look at the real frames.** Extract stills of the graded footage (or source if not graded): wide, tight, and any insert. Note wardrobe colours, wall/background colour, skin tones, where the face and hands sit, and how much clean space exists. Design must be derived from these frames, not imagined.
3. **Write the design constitution** to `PROJECT/.context/DESIGN.md` from [templates/design-constitution.md](templates/design-constitution.md). One page: tone in plain words, palette (5-6 named hex values with roles, sampled or derived from the footage, one accent family), type system (1-2 families, sizes, weights, tracking, Tamil fallback), surfaces (one card style, one shadow, one corner radius), icon/illustration system (one source, one style), motion grammar (one entrance, one exit, one emphasis move, easing values), caption policy, and a short "never in this video" list. Use [references/colour-and-surface.md](references/colour-and-surface.md), [references/typography.md](references/typography.md), [references/motion.md](references/motion.md).
4. **Self-review the constitution before building.** Compare every line against [references/anti-ai-tells.md](references/anti-ai-tells.md). Any choice that is a default you did not decide (Inter/Montserrat "because", indigo/violet, glass, glow, stripe gradient, emoji icons, sticker tilt on everything) must be justified by the brief or replaced. Write what changed and why in DECISIONS.md.
5. **Spec each beat's graphic.** For every graphic in the beat table add: its job (one of: guide the eye, emphasise a spoken word, show what footage cannot, bridge a cut; otherwise delete it), the exact motivating word and frame, the one focal point, entrance/hold/exit in frames, safe-area and face clearance. Layout and caption rules: [references/layout-and-captions.md](references/layout-and-captions.md). Icons, illustrations and AI inserts: [references/icons-images-and-ai-assets.md](references/icons-images-and-ai-assets.md).
6. **Build** with the project's chosen graphics route (Remotion/HyperFrames/native) and keep design tokens in ONE place in code (a single palette/type/shadow/easing object), never hex values scattered per scene.
7. **Audit the rendered frames, not the code.** Run the audit script on the actual draft or graphics render and look at the sheet:
   `E:/Video/.venv/Scripts/python.exe E:/Video/.claude/skills/video-design/scripts/design-audit.py VIDEO --out PROJECT/qa/design-audit --baseline PROJECT/work/aroll.mp4`
   (`--baseline` = the graded a-roll without graphics, optional; it stops footage colours such as a red shirt being blamed on the graphics. `--every 2` halves the time; a PNG folder also works with `--fps`.) It writes a contact sheet, a palette strip and `design-audit.json` (neon/oversaturated pixel share, distinct accent hues per frame, near-black/near-white extremes, banding risk) and prints flags. Calibration on 2026-10-26: the cinematic reference `references/Before n After (2).mp4` gives no flags; fresh-v1 flags a full-screen electric-blue wipe at 16 s, more than 4 accent hues in 45% of frames, 8 hue families overall and flat areas at banding risk. Numbers support judgement; they do not prove good design. Then walk the checklist at the end of [references/anti-ai-tells.md](references/anti-ai-tells.md) frame by frame on the sheet and at least five full-resolution stills (hook, densest graphic, split screen, insert, CTA). Record pass/issue per item in the project's qa notes.
   Lessons from the first real use (fresh-v2, 2026-10-26): (a) check a line against the transcript before calling it filler; two suspected filler lines were real translations. (b) A frame sheet at 25% size hides overflow; open full-size stills of every two-card or number-heavy beat (`₹36,000` overflowed its card and collided with the `=` disc). (c) SVG `feTurbulence` grain was nearly invisible (0.67 levels) and left a dot grid; a pre-made 512 px gaussian noise tile with `mix-blend-mode: hard-light` gave 1.96 levels (`work/design/make-grain.py` in img2442-fresh). (d) Measure grain/banding at native width; the audit now defaults to 1080. (e) Render the redesigned transition frames too, not only beat stills.
8. **Fix, then record.** Fix real issues at the token level (one change fixes every scene). Update DESIGN.md, DECISIONS.md and STATE.md. Do not claim motion was reviewed from stills; say what coverage was achieved.

## Decision order

Meaning and readability first, then the speaker's face, then consistency, then personality, then decoration. When in doubt remove the element: a beat with one strong idea on screen beats a beat with four competing ones.

## Boundaries

- Never change approved cuts, grade, captions wording or timing as a side-effect of a design pass; a design change that moves a cue needs a new timing revision.
- Do not install fonts or packages on C:. Fonts already on hand: E:/Video/.agents/skills/video-edit/assets/template/assets/fonts and the short-editing engine fonts; new Google Fonts files go into the project's own assets folder on E: with their licence noted.
- Upstream looks (video-edit's three looks, short-editing's paper system, HyperFrames blueprints) are vocabulary to borrow from, not presets.
- Research labels: the rules here come from design practice and published style guides (sources in [references/sources.md](references/sources.md)); they are not proof of retention or watch time.
