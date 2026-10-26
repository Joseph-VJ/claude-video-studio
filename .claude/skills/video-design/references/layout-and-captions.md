# Layout, safe zones and captions (1080x1920)

## 1. Safe zones

Studio working zone for organic Reels (from the video-edit layout rules, already used on IMG_2442): keep text and key graphics inside **x 35-980 (right 100 px clear from y ~1155 down), y 220-1470**.

Stricter zone when the video may also run as an ad, or must also work as TikTok/Shorts: Meta's published Reels ad margins are 14% top (~270 px), 35% bottom (~672 px, so content above y ~1248), 6% each side (~65 px). TikTok and YouTube Shorts ad templates are similar in height but want more side room (TikTok ~120 px each side, Shorts ~192 px on the right). These are ad specs; organic UI overlays are smaller, which is why the studio zone above is the default. Write which one applies in DESIGN.md.

Check, do not eyeball: render a few frames with a translucent red overlay of the unsafe area, fix, then render without it (video-edit `build.py --safe` pattern, or draw the overlay in the composition behind a debug flag).

## 2. Face and focal point

- The face is the trust signal. Keep eyes-to-chin clear of text and graphics at the tightest crop in the beat (check during motion, not one frame).
- Split screens: give the speaker at least ~45% of the frame height when they are talking about something personal or making a claim; inserts can take more when they show the proof.
- One focal point per frame. Decide it per beat and make everything else smaller, dimmer or absent.
- Eye trace: across a cut or scene change, put the new focal element near where the eye was (the speaker's eyes or the previous hero). Big jumps from top-left to bottom-right on every cut are tiring.

## 3. Grid and alignment

- Margins: one outer margin for all graphics (e.g., 64-80 px), one gutter. Things align to it.
- Prefer one strong alignment edge (left-aligned stack, or a centred axis) per scene, chosen on purpose. Everything-centred-and-symmetric is the generic default; left-aligned editorial blocks often read more designed.
- Size differences should be large and few. Avoid a row of three equal cards unless the speech literally lists three equal things.
- Inside a card, icon and text share a vertical centre; labels sit above or inside, never straddling an edge.
- Leave real empty space. A frame that is 30-40% empty around the focal element reads as confident.

## 4. Captions

Choose explicitly (director plan 7.3): verbatim, cleaned, translated keywords, emphasis-only, or none. Then:

- One caption style for the whole video: face, size, colour, treatment, position. Emphasis inside captions = the accent token only.
- Words per caption: 1-4 for word-by-word keyword style; up to ~42 characters per line and at most 2 lines for subtitle style.
- Reading speed for subtitle style: up to ~17-20 characters per second (Netflix: 20 cps adult, 17 cps children); minimum ~0.8 s on screen, maximum ~7 s.
- Position: a consistent band; for Reels typically between about 45% and 68% of frame height for subtitles, above the UI area, never over the face. Keyword captions may move with the composition but must return to the same band.
- Treatment: box or stroke for reliability (see typography.md section 6). Shadow alone fails on bright walls.
- Captions never sweep across the screen when a layout changes: fade out, wait for the layout, fade in at the new rest position.
- Captions and graphic text must not say different words at the same moment.

## 5. Phone check

- View the contact sheet at 25-35% size (roughly how it looks on a phone held at arm's length). Anything you cannot read there is too small or too thin.
- Check at least one frame on the actual phone if the user can, because displays and Instagram's compression change thin lines and saturated colours.
