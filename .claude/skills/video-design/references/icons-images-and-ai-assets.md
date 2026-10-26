# Icons, illustrations, photos and AI inserts

## 1. Do we need a picture at all?

A graphic must do one of four jobs: guide the eye, emphasise a spoken word, show what the footage cannot show, or bridge a cut. If an icon only decorates a word that is already on screen, delete it. The speaker's face and gesture are often the best "graphic".

## 2. One visual system per video

Pick ONE in DESIGN.md:

- **Drawn line/shape icons** made for this video: same stroke width (e.g., 6-8 px at 1080 width), same corner style, palette colours only, drawn on with a stroke animation where it helps.
- **Real object cut-outs**: photos of real things (a loan file, a phone with an app, a bank door) with the background removed (/remove-background), a consistent paper/white border or contact shadow, optional halftone.
- **Paper collage / illustration library**: one illustration style reused across the channel (short-editing podcast library, /vox paper collage).
- **Recreated UI**: a real-looking app/bank/CIBIL screen recreated in HTML with system fonts and plausible but clearly illustrative data (never fake a real brand's screen with invented numbers presented as real).

Never mix systems in one video. Never use glossy 3D emoji clip-art, generic avatar people, stock map pins, light bulbs for "idea", money bags with flying coins, hourglasses for "time", gauges for "rate", or Noto emoji images unless the user asks for that look.

## 3. People and "Customer A/B"

- Prefer: the speaker indicating with a gesture, two simple labelled silhouettes cut from one photo style, initials in plain shapes, or two real-looking stills generated with consistent un-idealised styling.
- Avoid: flat cartoon avatars with ties, emoji faces, mismatched skin tones between the two characters unless meaningful.

## 4. AI-generated inserts (images and clips)

The user generates manually (/request-video-assets, /image, /video). To keep them from reading as AI:

At prompt time (/image references/de-slop.md owns the details):
- Describe the capture medium as a fact ("phone video", "handheld footage"), real located imperfections, muted natural grading, ordinary people and places that match the audience (Indian bank branch, real office clutter, real paperwork).
- Match the a-roll: same light direction/temperature where plausible, similar contrast and grain.
- No booster words (4K, ultra-detailed, cinematic, stunning). No text inside generated images; add text in the edit.

At integration time:
- Inspect at full resolution: hands, teeth, eyes, garbled signage, impossible geometry, plastic skin, too-perfect symmetry. Reject or crop around problems.
- Neutralise, then grade to the a-roll look; add matching grain and slight softness if the clip is sharper than the a-roll.
- Keep generated clips short (about 1.5-3 s in a Reel) and cut on motion; long holds expose drift.
- Crop tighter than the generator's composition; centred, symmetrical generator framing is itself a tell.
- Use a consistent window/frame treatment from DESIGN.md.
- Keep provenance (asset manifest) and preserve originals.

## 5. Logos and real brands

- Use real logos only when spoken about and only flat (no added glow/bevel). Do not invent brand marks.
- Bank or app names on screen must match what was actually said.
