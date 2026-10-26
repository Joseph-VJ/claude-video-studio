# Design constitution — img2442-fresh v2 (design pass on fresh-v1)

Video: E:/Video/IMG_2442.MOV (Tamil, tripod, blue suit) · Date: 2026-10-26 · Revision: d1
Scope: SAME-PROJECT polish of fresh-v1. VJ loves fresh-v1 and v12, so the cut, beat plan, event timings, camera, grade, AI inserts, sound and copy are unchanged. Only the drawn layer changes (tokens, backdrop, chips, icons, motion, transitions). Source of v1 graphics kept in work/design/src-v1.

## Tone in plain words
Trustworthy, direct, local, energetic. A consultant explaining money to first-time borrowers: paper and ink with one warm accent, not a tech startup. Energy comes from motion timed to the voice, not from effects.

## Built from these frames
work/design/aroll-12.png and aroll-45.png (graded a-roll). Cream wall #CBBDB2–#D8C9BE, cobalt satin suit #344888–#405EB1, white shirt #DCE1E6, warm wood desk, teal-grey tablet case, dark brown skin. Clean space: upper 30% of the frame is empty wall.

## Palette (one family of ground, one accent, two story colours)
| Token | Hex | Role | Where it came from |
|---|---|---|---|
| ground | #22326A (range #27397A top to #1B2759 bottom) | backdrop behind speaker windows and full cards | deepened suit blue, hue 227°, S .68 V .42 (v1 used #2457FF, S .86 V 1.0 plus stripes) |
| ink | #14193A | text on paper/accent, dark chips | tinted navy-black, never #000 |
| paper | #F3EADC | cards, chips, plain text on ground | the cream wall, lightened |
| accent | #E5A63A | ONE punch word / hero number per beat | warm complement to the suit; echoes wood and skin warmth |
| alert | #B13B34 | problem / villain: Customer A, EMI, "BUT…" wash (#7E3733) | brick, S .69 V .69 |
| good | #3FB594 | good outcome: Customer B, ticks, call | hue of the tablet case, lifted for contrast |
Proportion: ground and footage ~90%, paper ~7%, accent ~3%. alert and good appear only in comparison and outcome beats; most frames show ground + paper + one accent. Good vs bad is also carried by position (A left, B right), tick vs cross and size, not colour alone.
Contrast (measured): paper on ground 10.2, accent on ground 5.7, good on ground 4.8, ink on accent 8.0, ink on good 6.7, paper on alert 5.0, ink on paper 14.3. Chips over the cream wall use ink (ink vs wall 10.6); paper vs wall is only 1.35, so paper chips are used on ground only.

## Type: one family, Archivo (variable weight and width, SIL OFL, file public/fonts/Archivo.ttf)
| Role | Weight | Width | Size px | Tracking |
|---|---|---|---|---|
| hero word / number | 800 | 82% | 150–250 | -1% |
| headline chip | 800 | 85% | 84–130 | -1% |
| keyword chip | 800 | 90% | 54–74 | 0 |
| label | 600 | 100% | 30–44 | +8%, caps |
| Tamil | 700 Nirmala UI | — | 110 | 0, line-height 1.35 |
Numbers: Archivo tabular figures, ₹ and Indian grouping as spoken (₹1,00,000; ₹36,000; 6 L, 9 L). Emphasis: one accent chip or accent-coloured word per beat; everything else plain or ink/paper chips. v1's Inter Tight 900 on every label is retired.

## Surfaces
Card radius 28, chip radius 18, speaker/clip window radius 40 (bubble stays a circle). One light from above: shadow low `0 6px 16px rgba(10,14,40,.30)`, high `0 18px 44px rgba(10,14,40,.38)`. Windows: 4px paper border at 92%, no coloured rings. Flat fills only (no gradients on cards, bars, coins). Backdrop: ground gradient within one hue, fine animated grain 7% soft-light (also prevents H.264 banding), one slow light sweep at 5% opacity. Removed: diagonal stripes, dot grid, floating ₹ % ✓ watermarks, coloured radial glow.

## Pictures: one system, flat drawn shapes
Flat vector, palette colours only, stroke 8 px. Customer A/B = letter discs (no cartoon avatars). Building = flat paper silhouette with ground windows. Coin = flat accent disc with ink ₹ (coin stack for ₹1 L). Where? = three paper icon tiles (bank, app, company). Removed: glossy coin bag, light bulbs, map pins, sparkles, confetti bursts, floating question marks.

## Motion grammar
Entrance: rise or slide 40–160 px with fade and 3% scale, 12 frames, `cubic-bezier(.16,1,.3,1)` (expo out). Exit: 5 frames, accelerating, 16 px lift. Numbers: count up on the stress with cubic ease-out, hold ≥ 1 s. Stamp (declared accent, only "GOOD LIST ✓" and "₹0 COMMISSION"): lands with a thud, 6° tilt, no bounce. Scene change: backdrop windows morph as in v1; transitions are ground-colour wipes with a paper hairline, ground-colour slices, an ink iris with a paper ring, and a soft paper flash (≤50%). Camera punches are unchanged (compose.py). Removed: spring overshoot, shake, wobble bob, shock rings, speed lines, RGB glitch bars, white strobe, gold wipe stripe.
Sound: unchanged in this pass. Recommendation for a later pass: thin the SFX (the same whoosh on most transitions) by about a third.

## Layout and captions
Safe zone: studio organic (x 35–980, y 220–1470). Graphics sit where v1 put them; face clearance unchanged (graphics above the head or in windows). Copy is unchanged and each line was kept: "AND MORE…" and "WHO GOT MORE?" are real translations (இப்படி நிறைய விஷயங்கள் இருக்கு; யாருக்கு அதிகமா லோன் கிடைச்சது).

## Never in this video
Glow or bloom; neon or fully saturated fills; stripe or multi-hue gradients; glass cards; emoji or glossy 3D icons; cartoon avatars; sparkles, confetti, shock rings, speed lines; hard offset text shadows; spring overshoot; more than one highlighted word per beat; tilt except the two stamps.

## Code location of tokens
src/kit.tsx exports `T` (colours), `R` (radii), `SH` (shadows), `ease*` and the `Chip`, `Card`, `Pop`, icon components. src/index.tsx holds the backdrop and transitions and reads only `T`. No hex values in src/scenes.tsx.

## Beat jobs (what each graphic does)
Every graphic is kept for one of: show what the footage cannot (numbers, comparison, chart), emphasise a spoken word (hero chips), guide the eye (chevrons, tick order), bridge a cut (wipes). Removed because they did none: sparkles, confetti, shock rings, speed lines, floating ?, bulbs, coin bag, map pins, ghost "?" pulse, background watermark symbols.

## Audit results (preview stills, 24 per-beat frames, native 1080 width; not motion)
| Measure | fresh-v1 stills | fresh-v2 stills |
|---|---|---|
| max neon pixel share in a frame | 7.8% | 0.05% |
| frames with more than 1% neon pixels | 17% | 0% |
| mean oversaturated share | 10.4% | 5.9% |
| accent hue families across the set | 10 | 7 |
| max accent hues in one frame | 8 | 6 |
| frames with more than 4 accent hues | 58% | 42% (all A-red / B-green comparison beats or beats with AI clips and footage) |
| ground grain at native resolution (block std, levels) | stripes 2.0 | grain 1.96 (colour unchanged) |
Whole-video audit of fresh-v1 (qa/design-audit-v1): full-screen #2457FF flood at 16 s, more than 4 hues in 45% of frames, 8 hue families. Stills: qa/design-audit-stills-pv (v1) and qa/design-audit-stills-pv2 (v2). Review images: E:/Video/out/review/fresh-v2-*.png. fresh-v2 full video not rendered yet; audit it with --baseline work/aroll.mp4 after the render.
Not checked: motion of the new easing and transitions in real time, contrast on the brightest frame behind chips over the wall beyond the sampled stills, Tamil end-card spelling by a Tamil reader, the "BUT…" wash in motion.
