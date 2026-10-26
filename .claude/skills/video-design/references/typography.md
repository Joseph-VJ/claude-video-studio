# Typography for vertical video

Type is most of the design in a talking-head Reel. It decides whether the video looks like this speaker's channel or like a caption app preset.

## 1. Choose the faces on purpose

- One family, or two clearly different ones (a heavy grotesk + a serif or script for one accent word). Never three.
- Choose for the speaker and subject: a finance consultant explaining loans to first-time borrowers wants credible, warm, plain-spoken type, not tech-startup type or meme type. Write the reason in DESIGN.md in one line.
- Inter, Inter Tight, Montserrat and Poppins are not banned, but they are the most common defaults in generated design. If one of them is used, the identity must come from scale contrast, tracking, a second accent face and a strict colour system, not from the font. Otherwise prefer a face with more character.
- Fonts already on this PC (OFL, no download needed):
  - Display/grotesk: Bricolage Grotesque, Archivo, Archivo Black, DM Sans, Inter Tight 800/900, Bowlby One SC (poster only), Montserrat 500/600 (labels only)
  - Serif/accent: DM Serif Display (+italic), Instrument Serif (+italic)
  - Hand/script: Caveat 600 (notes and arrows only), Meie Script (projects/img2442-motion-v1/public/fonts, one accent word only)
  - Condensed poster: Anton (projects/img2442-motion-v1/public/fonts; the video-edit upstream lists it as "looked worse"; use only when the brief asks for poster energy)
  - Mono: JetBrains Mono (numbers in UI recreations only)
  - Tamil: Nirmala UI (C:/Windows/Fonts/Nirmala.ttc) is installed. Better Tamil display options (Noto Sans Tamil, Hind Madurai, Mukta Malar, Catamaran) are free from Google Fonts but must be downloaded into the project's assets/fonts folder on E: only after the user approves the download.
  - Paths: E:/Video/.agents/skills/short-editing/engine/fonts and E:/Video/.agents/skills/video-edit/assets/template/assets/fonts.
- Render check: Remotion/HyperFrames silently fall back when a font fails to load. Confirm the face in a full-resolution still (compare letter shapes such as "g", "R", "₹"), never trust the CSS.

## 2. Scale and hierarchy (1080x1920)

Pick a small scale and stay on it. Suggested starting scale, adjust per face:

| Role | Size px | Weight | Notes |
|---|---|---|---|
| Hero word / number | 180-260 | 800-900 | one per beat, the thing the viewer should remember |
| Headline line | 96-140 | 700-900 | 1-2 lines, up to ~16 characters per line |
| Caption / spoken keyword | 64-96 | 700-800 | about 3-5% of frame height; bigger only if it IS the beat |
| Label / tag | 34-44 | 500-600 | caps with +6-12% tracking |
| Minimum anything | 34 | — | smaller is unreadable on a phone |

- Size difference shows importance; avoid five near-equal sizes on one frame.
- Numbers are heroes in money content: set ₹ and digits in one consistent style (same face, weight, colour) for the whole video. Use tabular figures when numbers count up. Use Indian grouping (₹1,00,000 / ₹9 L) consistently; do not mix "1 lakh", "1L" and "1,00,000" in the same video unless the speech does.

## 3. Spacing

- Display sizes (over ~90 px) usually want negative tracking around -2 to -4% of size; body sizes 0.
- ALL CAPS needs positive tracking, about +5 to +12%, and only for short labels. Do not set long phrases in caps.
- Line height: 0.9-1.0 for big display lines, 1.15-1.3 for anything readable as a sentence. Caps lines can look looser than mixed case; adjust by eye.
- Kerning: inspect pairs like AV, LT, ₹ followed by a digit, and digits next to "L". Fix visible gaps in big type.
- Line breaks: keep noun + adjective, number + unit, ₹ + amount, first + last name together. Prefer a bottom-heavy two-line shape; never leave one short word alone on a line.

## 4. Emphasis

- One emphasis per beat: colour, weight, or the accent face, not all three.
- Emphasis follows the speech stress. The stressed word gets the weight; filler words ("in", "the", "a") never do.
- Highlight pills/boxes: at most one per beat, and only for the punch word. Plain type is the default.
- Italic/script accent: one word, used the same way every time (e.g., only for the "good outcome" word).

## 5. Tamil and bilingual text

- Tamil vowel signs and conjuncts need more vertical room: line height at least 1.3 for Tamil; check that marks above and below are not clipped by masks or boxes.
- Do not fake bold or condense Tamil; use a font that has the needed weight.
- Do not mix Romanised Tamil with English keywords in one caption line unless the brief asks for it.
- Keep translation accuracy separate from design: a beautiful wrong word is still wrong.

## 6. Text on footage

- Treatments in order of reliability: solid or near-solid box behind text, then a 3-6 px dark stroke (scaled to size), then a soft shadow as a supplement only. A shadow alone fails on bright walls.
- Test contrast on the brightest background frame behind the text, not a mid frame. Target at least 4.5:1 for normal text and 3:1 for large display text (WCAG thresholds used as a practical check).
- Never place text over the eyes-to-chin region of the speaker. Text may sit over the chest or behind the head only if it remains readable (see video-edit references/layout.md formula).

## 7. Reading time

- Spoken-keyword captions can follow the voice word by word. Anything the viewer must READ beyond the voice (a list, a number with a condition, a comparison) needs time: about 15-20 characters per second is a comfortable adult reading speed (Netflix caps adult subtitles at 20 cps), plus about 0.3 s to find the text.
- A hero number should hold at least ~1 s after it settles.
