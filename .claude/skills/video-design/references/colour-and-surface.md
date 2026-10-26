# Colour of graphics, backgrounds and surfaces

This file is about the colour of what we DRAW. The grade of the footage belongs to the colourist lane (director plan section 8); graphics must sit with that grade, not fight it.

## 1. Derive the palette from the footage

1. Pull 4-6 graded stills (wide, tight, insert). Sample: wall/background, wardrobe main colour, wardrobe secondary (shirt), skin mid-tone, any prop colour.
2. Build 5-6 named tokens with roles:
   - `ground`: backdrop for full-screen cards. A tone that belongs to the set (wall cream, a darkened wardrobe colour, warm paper), not a stock gradient.
   - `ink`: text colour on ground, a tinted near-black (not #000).
   - `paper`: card/sheet colour, a tinted near-white (not #FFF), or the inverse for dark looks.
   - `accent`: ONE colour for the punch word / hero number. Pick from the footage (e.g., the suit blue, deepened) or a deliberate complement to skin and set.
   - `alert`: one warning colour for the problem/villain, used rarely.
   - `muted`: secondary text/lines.
3. Rough proportion across the video: ground/neutrals ~60%, footage/secondary ~30%, accent ~10% (the 60-30-10 guideline from film and design practice; a guide, not a formula).
4. Good/bad does not need red/green. Shape (cross vs tick), position (left vs right), strike-through, dimming, or size can carry it, so the palette stays small. If red/green is used, use the same two values everywhere.
5. Record hex values in DESIGN.md and in ONE token object in code.

## 2. Saturation and the neon limit

- Neon = very high saturation AND very high brightness in the same pixel. On phones it vibrates, blooms and looks generated.
- Working limit for drawn graphics (HSV, 0-1): saturation <= ~0.80 when value >= ~0.85. Large fills (backdrops, big cards) <= ~0.60 saturation.
- Yellow is the exception that most often goes neon; prefer warm yellows (#F2C94C-type) over lemon (#FFE600).
- `design-audit.py` reports the share of neon pixels per frame. Real footage rarely produces any; drawn graphics should keep it near zero.
- Saturated accents are fine as small marks (a word, an underline), not as full-screen floods. Full-screen colour washes should be deep or desaturated.

## 3. Backgrounds for full-screen cards

Prefer, in order:
1. The real scene: blurred or darkened a-roll, a crop of the set, or a supplied/AI plate graded to the a-roll.
2. A flat `ground` tone with fine grain (1-2%) and an optional very slow light drift.
3. A one-hue gradient (two close tones) with grain to prevent banding.

Avoid: multi-hue gradients (blue-purple-pink), diagonal stripe patterns, floating currency/percent watermarks, pastel blobs, particles, bokeh, lens flares, grid-of-dots "tech" textures, unless the brief explicitly asks for that world.

## 4. Surfaces: cards, windows, chips

- One card style for the video: one radius (e.g., 18-28 px at 1080 width, or 0 for an editorial look), one border treatment (none or a hairline in a palette tone), one fill.
- One light: all shadows fall the same direction. Define at most two elevations as tokens, e.g. `low: 0 2px 6px rgba(ink,.18)` and `high: 0 18px 40px rgba(ink,.22)` plus a tight contact shadow. Never invent a new shadow per scene.
- No glow, no outer light, no inner glow, no neon stroke.
- No glassmorphism over moving footage unless contrast is verified on the brightest frame; opaque paper/ink cards are the default.
- No nested cards, no cards with a coloured left border, no rounded icon tile above every heading.
- Speaker windows (split, inset): one radius, one border, consistent across the video. A hairline or thin paper border reads cleaner than a thick coloured frame.

## 5. Texture and "made by hand"

Grain and slight imperfection are the strongest cheap signals that a person made the frame; they also hide 8-bit banding.

- Add uniform fine grain (about 1-3% amplitude, monochrome) over drawn backdrops and gradients, matched in size to the footage's noise.
- Optional, when the tone fits: paper texture, torn/deckle edges, halftone print on cut-outs, hand-drawn underline/arrow strokes (Caveat or SVG stroke draw-on), stop-motion steps at 12 fps for collage pieces (the Vox-explainer feel). Pick one of these per video, not all.
- Do not add film grain on the speaker's face if it reads as noise (video-edit upstream note); grain is for the drawn layer and inserts.

## 6. Graphics and the grade

- Grade footage before graphics; graphics are not graded afterwards (director plan section 8 point 8).
- Check that graphic colours still look right next to skin: an accent near the face's hue makes skin look orange; a cold cyan next to warm skin can make it look grey.
- Inserts (AI or stock) are colour-matched to the a-roll: neutralise first, then apply the same look, then compare side by side on one still.

## 7. Banding check

- Wide smooth gradients and dark vignettes band after H.264 8-bit export. Grain/dither before the final encode is the fix; the exporter is not a fix.
- Inspect the darkest and smoothest graphic frame of the exported file at 100% (the audit json `banding_risk` flags frames with large smooth areas; confirm by eye).
