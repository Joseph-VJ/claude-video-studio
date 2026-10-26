# Motion grammar

Movement is cheap; timing is the craft. The difference between template motion and designed motion is mostly easing, timing to the voice, and restraint.

## 1. Define the grammar once

In DESIGN.md write one of each, used everywhere for the same role, so the viewer learns the language:

- Entrance (e.g., rise 24-60 px + fade, or a mask wipe, or a hard cut-in on the syllable)
- Exit (shorter, cleaner: fade + small lift, or cut)
- Emphasis (one move for the punch word: weight/colour change, underline draw-on, scale 1.00 -> 1.06 settle)
- Number behaviour (count-up with its unit, or a hard set; never sitting on 0 before it is spoken)
- Scene change (hard cut, push, or a shared-element morph when the next beat shows the same object bigger)
- Camera on the speaker (punch-in for emphasis or to hide a jump cut, slow push on holds)

## 2. Easing (CSS cubic-bezier values; GSAP equivalents in brackets)

| Role | Curve | Notes |
|---|---|---|
| Entrance | `cubic-bezier(0.16, 1, 0.3, 1)` (expo.out / power4.out) | front-loads travel, decelerates into place |
| Gentle entrance for big type | `cubic-bezier(0.22, 1, 0.36, 1)` (power3.out) | |
| Exit | `cubic-bezier(0.7, 0, 0.84, 0)` (power3.in) | accelerates away; exits feel final |
| Move/scale in place | `cubic-bezier(0.65, 0, 0.35, 1)` (power2.inOut) | |
| Spring | critically damped, no overshoot | if springs are used, damping high enough that nothing passes its target |

Avoid by default: linear (mechanical), bounce, elastic, back/overshoot, wiggle, shake, pulse, spin. These are the template signature. One deliberate overshoot accent per video is allowed if DESIGN.md names it.

## 3. Durations at 30 fps

| Move | Frames | Seconds |
|---|---|---|
| Small label/word entrance | 6-9 | 0.20-0.30 |
| Card / window entrance | 9-15 | 0.30-0.50 |
| Full-screen scene entrance | 12-18 | 0.40-0.60 |
| Exit | ~75% of its entrance, usually 5-9 | 0.16-0.30 |
| Stagger inside a group | 2-4 per item | |
| Hold after settle for a hero number | >= 30 | >= 1.0 |
| Slow push on a held board | 1.00 -> 1.025-1.04 over the hold | |

Exits are shorter than entrances and finish at exactly 0 opacity (no ghost frames bleeding into the next beat). Beats are sequential on the same layer: the next element enters after the previous one has left, not as a muddy crossfade.

## 4. Timing to the voice

- Every entrance lands on the frame of its motivating stressed syllable (from word timings), within +/- 2 frames. Being 3-4 frames late is what makes motion feel placed rather than designed.
- Read word timings from the project's transcript; check the actual waveform at critical hits.
- Let pauses breathe: when the speaker pauses on a key line, the graphic holds too.

## 5. How much moves

- One focal mover at a time. Secondary elements settle 2-4 frames after the primary (overlapping action), not simultaneously.
- A move uses one or two properties (position + opacity, or scale + opacity). Animating many properties at once looks busy.
- Constant motion inside a beat is welcome (VJ's 3-second preference: visuals change about every 3 s with motion inside), but each motion must reveal or emphasise something said. Idle drifting decoration is not motion design.
- Before final render, look for anything that moves without a job and delete it. Removing roughly a third to a half of first-pass moves is normal.

## 6. Motion blur

- Rendered graphics have zero exposure time, so fast moves look razor sharp and "web". For moves faster than about 40 px per frame, add directional blur equivalent to a ~180° shutter (blur length about half the per-frame travel), or draw it in the composition (a CSS `filter: blur()` on the moving axis scaled to speed, or several low-opacity trailing copies). `@remotion/motion-blur` is NOT installed in projects/renderer or img2442-fresh; installing it is a new package and needs the user's go-ahead. Keep slow text moves sharp.
- Check blur on a full-resolution still from the middle of a fast move.

## 7. Transitions

- Motivate a transition with something in the frame: a gesture, a moving object, a shape that continues, a hard cut on a beat.
- Avoid preset wipes, glitches, light leaks, star/page-curl/spin transitions and RGB-split unless the brief wants that world.
- A jump cut hidden by a punch-in should change scale by a visible amount (>= ~6%) and keep the eyes near the same screen position (eye trace).

## 8. Sound pairing

- A sound cue belongs to a real visual event (a reveal, a stamp, a cut that changes idea). Not every label needs one.
- Align the transient to the visual hit frame; tens of milliseconds matter.
- Vary the cue family; the same whoosh on every cut is a template tell. Delete 30-50% of a first SFX pass and keep the ones that change understanding or feeling.
- Voice stays dominant; effects and music sit well below speech (director plan section 9 governs loudness).
