# AI tells in video design, and what to do instead

A "tell" is a choice that looks defaulted rather than decided. One tell alone rarely ruins a video; four or five together make it read as a generated template within a second. Each row says what it looks like, why it reads as AI, and the replacement. "Seen" marks where it appeared in our own drafts (from the source code of projects/img2442-fresh and stills of out/IMG_2442-edited-v12.mp4), so we fix the habit, not just the example.

Remember the scope: VJ loves fresh-v1 and v12. Keep their structure and energy. Fix the tells inside it.

## 1. Colour and light

| Tell | Why it reads as AI | Do instead | Seen |
|---|---|---|---|
| Neon accents: pure, fully saturated hues (#FF2BD6 magenta, #22D3A0 mint, #FFE600 lemon) | Generated UI and thumbnails max out saturation because it "pops"; real designers tune accents to the footage | Accents at saturation 55-80% and value 75-92% in HSV; one accent family per video; pick it from or against the footage (wardrobe, set) | fresh-v1 used all three |
| Rainbow semantics: a different accent for every idea (red, green, yellow, blue, purple, orange) | Looks like an icon pack, not a brand | 1 accent + 1 warning colour + neutrals. Good/bad can be shown with shape, position or strike-through instead of red/green | fresh-v1 had ~25 distinct hex values; v12 red/green/orange/blue/purple |
| Indigo/violet/royal-blue gradient backdrops, especially with diagonal stripes or floating ₹/% watermarks | The single most recognised AI default (Tailwind indigo-500 #6366F1, violet-500 #8B5CF6 and relatives) | Flat backdrop taken from the scene (wall cream, suit navy darkened, paper), or a real photographic/texture plate; if a gradient, a subtle one within one hue, plus grain | fresh-v1 royal-blue stripes with faint ₹ |
| Glow, bloom, outer light halos, "dark glows" behind cards or text | Signature of generated sci-fi/tech design; it also blooms on phone screens and compresses badly | Separation by contrast, a single soft contact shadow, or a scrim | fresh-v1 had glow effects |
| Glassmorphism: frosted translucent cards | Popular default in AI UI output; on moving footage it lowers text contrast unpredictably | Opaque or near-opaque paper/ink cards; if translucency is wanted, test contrast on the brightest frame behind it | fresh-v1 "glass cards" |
| Pure #000 / pure #FFF everywhere, or grey text on a coloured card | Flat and digital; grey-on-colour fails contrast | Tinted neutrals derived from the palette (ink #1B1B24-type, cream instead of white); text on colour is ink or white tested for contrast | partly |
| Pastel blobs and confetti dots floating in the background | Decorative filler with no meaning | Remove, or replace with a real object from the story | v12 purple/peach blobs |
| Smooth wide gradients that band after H.264 | Reads as cheap and digital | Add 1-2% grain/dither over gradients; prefer flat fields | risk on any gradient |

## 2. Type and copy

| Tell | Why | Do instead | Seen |
|---|---|---|---|
| Inter / Inter Tight / Montserrat / Poppins chosen by default for everything | The most-sampled fonts; the type has no voice of its own | Choose type for the speaker and topic (see typography.md); if Inter-family stays, earn it with deliberate scale, tracking and a contrasting second face | fresh-v1 Inter Tight 900 everywhere |
| Every keyword in a yellow highlight pill, tilted sticker or badge | Template-pack habit; when everything is highlighted nothing is | Plain set type for most words; reserve a highlight treatment for ONE word per beat at most | fresh-v1 almost every label |
| Mixed treatments per scene (pill, sticker, outline, box, ribbon, bar) | No system, so the eye relearns every 3 s | One label style, one number style, one emphasis style for the whole video | fresh-v1, v12 |
| Filler copy (generic engagement phrases with no source in the speech, e.g. "AND MORE..." where nothing was said) | A model writes these when it has no content | Words from the speech, or a concrete number/noun; check each line against the transcript before judging it filler (fresh-v1's "AND MORE..." and "WHO GOT MORE?" turned out to be real translations of the Tamil and were kept; only the floating "?" decorations were tells) | checked 2026-10-26 |
| Title Case or ALL CAPS on everything with default tracking | Caps need +5-12% tracking; default-tracked caps look cramped and generated | Caps only for short labels with added tracking; big words can be sentence case | both |
| Emoji characters typed into text | Device-dependent rendering, instantly casual | Drawn icon or word | — |

## 3. Icons, illustration and imagery

| Tell | Why | Do instead | Seen |
|---|---|---|---|
| Glossy 3D emoji clip-art (money bag with coins, light bulb, map pins, hourglass, gauge) | Stock emoji packs and AI icon generators produce exactly these; they look like a slide template | One icon system drawn for the video (consistent stroke, corner and fill), or a real object photo cut out, or no icon | fresh-v1 and v12 |
| Generic flat avatar people (round head, tie) for "Customer A/B" | Clip-art people carry no identity | Silhouette cut from a real or generated photo with consistent styling, initials in a simple shape, or the speaker's own gesture | both |
| Mixed icon styles (flat + 3D + line + emoji) in one video | No system | Pick one style for the whole video | v12 |
| Rounded-square icon tile above every heading; three equal cards in a row | Card-kit reflex learned from tutorials | Asymmetric layout driven by the content; an icon only when it adds information | v12 three cards |
| Sparkles ✦, floating question marks, check-mark badges on everything | Decoration standing in for meaning | Delete; use motion of real content for energy | fresh-v1 |
| AI images/clips that are too sharp, too saturated, symmetrical, with plastic skin, perfect office, smiling headset agent | AI imagery prior toward idealisation; mismatched with the real a-roll | Grade inserts to the a-roll, add matching grain/softness, crop tighter, keep under ~3 s, request un-idealised prompts (/image de-slop) | consultant insert |

## 4. Surfaces and layout

| Tell | Why | Do instead | Seen |
|---|---|---|---|
| A different shadow on every element | Each scene invented its own; nothing feels lit by one light | One shadow token (or two elevations) for the whole video, from one light direction | fresh-v1 had 10+ boxShadow variants |
| Big radius on everything, cards inside cards, coloured left border on cards | Generic UI-kit look | One radius; no nested cards; borders only when they carry meaning | v12 left-border cards |
| Everything centred, symmetrical, same size | Statistically safe layout | Use a grid with one strong alignment edge; let size difference show importance | both |
| Speaker shrunk into a tiny bubble while a backdrop fills the screen | Face is the trust signal for this audience; tiny bubbles feel like a template | Keep the face large; split screens give the face at least ~45% of height | fresh-v1 bubble beats |

## 5. Motion

| Tell | Why | Do instead | Seen |
|---|---|---|---|
| Bounce, elastic, overshoot, spring "pop" on every entrance | The template signature; feels dated and ignores the voice | Decelerating ease-out entrance, shorter accelerating exit, overshoot only for one deliberate accent | fresh-v1 used bounce/overshoot/spring |
| Every element enters at once, or everything wiggles | No focal point | One mover at a time; stagger 2-4 frames inside a group | — |
| Linear motion and perfectly sharp fast-moving graphics | Mechanical, "web animation" feel | Eased curves; directional motion blur on fast moves (approx. 180° shutter) | — |
| Motion that misses the syllable | A preset was placed, not timed | Land the entrance on the stressed syllable's frame (word timings) | — |
| Same zoom/punch on every stressed word | Mechanical rhythm | Punch only for emphasis or to hide a cut; vary scale with meaning | earlier v7 |
| Whoosh on every transition, ding on every label | Sound template | Sound only for real visual events; delete 30-50% of a first SFX pass | check each draft |

## 6. Final checklist (walk it on the rendered contact sheet and stills)

Mark each item pass / issue / not checked in the project's qa notes.

1. Can you name the palette in five hex values, and does every frame use only those? (audit json: distinct accent hues)
2. Is any graphic pixel neon (audit: neon share near zero outside real footage)? Any glow or halo?
3. Is there exactly one focal point per frame? Is the face large and unobstructed when the speaker is the point?
4. Do all labels share one style, all numbers one style, all icons one style, all cards one radius and shadow?
5. Is every word on screen either spoken or a concrete number/noun from the speech? Any filler phrase?
6. At most one highlighted word per beat?
7. Caps tracked, line breaks sensible, Tamil glyphs rendered correctly, text readable on a phone at arm's length (view the sheet at 25% size)?
8. Text contrast holds on the brightest frame behind it?
9. Inside safe zone (layout-and-captions.md) and clear of eyes-to-chin?
10. Inserts graded and textured to sit with the a-roll; no plastic skin, garbled text or extra fingers?
11. Entrances eased and on the syllable, exits shorter, no bounce/elastic except a declared accent, fast moves blurred?
12. Could this frame appear in a stock template pack? If yes, what would make it belong only to this speaker and this story?
