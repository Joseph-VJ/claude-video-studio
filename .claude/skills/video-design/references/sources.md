# Research sources (read 2026-10-26)

Evidence labels: **Standard** = published style guide or spec; **Practice** = designer/editor guidance, blogs, vendor articles (directional, often with a commercial interest); **Observed** = our own drafts. None of these establishes a retention or watch-time effect.

## Why AI design looks generic
- Practice: 925 Studios, "AI Slop Fonts and Gradients: The Tells That Give Away AI Design" — Inter by default, indigo/purple gradients, three equal cards, generic line icons, vague headlines; fix by constraining type/palette/layout and auditing. https://www.925studios.co/blog/ai-slop-design-tells
- Practice: Superdesign, "Why AI Design Looks Generic (2026)" — stock Tailwind hues (#6366F1, #8B5CF6, #A855F7), glassmorphism, rounded everything, 0.1-opacity shadows, badge above headline; separate taste direction from build, pin a spec. https://superdesign.dev/blog/why-ai-design-looks-generic
- Practice: Indie Hackers, "The AI Purple Problem". https://www.indiehackers.com/post/the-ai-purple-problem-why-every-ai-brand-looks-the-same-6cb0aa2a02
- Practice: Anthropic frontend-design skill (github.com/anthropics/skills) — commit to a direction drawn from the subject's world, small token system (4-6 hex), one orchestrated motion moment, self-review the plan for defaults, remove one element before finishing.
- Practice: Impeccable design skill (github.com/pbakaus/impeccable) — detector rules incl. purple-blue gradients, dark glows, pure black/grey, nested cards, icon tile above headings, bounce/elastic easing "feels dated".

## Motion
- Standard: Atlassian Design System, "Applying motion" — ease-out entrances, ease-in exits, exits 50-100 ms shorter, one or two properties per transition, same role = same motion. https://atlassian.design/foundations/motion/applying-motion
- Practice: withmedia, "Motion Graphics That Don't Look Like Templates" — land type on the stressed syllable (4 frames late feels cheap), retire elastic bounce, one entry behaviour, visual constitution per client, every graphic needs a job, delete about half. https://withmedia.in/blog/motion-graphics-not-templates
- Practice: Vision Labs, "AI motion design in 2026" — precise easing values and frame-timed beats beat adjectives; reference still anchors quality. https://www.visionlabs.studio/blog/ai-motion-design-state-of-the-art
- Practice: SpaceX Animation, easing and timing as the cheap/expensive difference. https://spacexanimation.com/why-some-animation-feels-expensive-and-some-feels-cheap-the-science-of-easing-and-timing/
- Practice: PremiumBeat on 180° shutter / motion blur, and on Vox-style 12 fps graphics. https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/
- Practice: Envato, "11 Motion Design Trends for 2026" — authenticity through imperfection, craft as luxury (hand-made, stop-motion, visible texture), minimal editing. https://elements.envato.com/learn/motion-design-trends

## Type, captions, reading
- Standard: Netflix English (USA) Timed Text Style Guide — 42 characters per line, 20 cps adult / 17 cps children, max 2 lines, line-break rules. https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
- Practice: Blitzcut, caption professionalism — box > stroke > shadow, size and placement bands, 1.5-6 s per block. https://blitzcutai.com/blog/how-to-make-captions-look-professional
- Practice: Typography for Lawyers and Pimp my Type — +5-12% tracking for caps; negative tracking only at display sizes. https://typographyforlawyers.com/letterspacing.html · https://pimpmytype.com/spacing-all-caps/
- Practice: Tamil faces — Hind Madurai, Noto Sans Tamil, Mukta Malar, Catamaran (Adobe Fonts / Google Fonts listings). https://fonts.adobe.com/fonts/hind-madurai
- Standard (applied as a practical check): WCAG 1.4.3 contrast 4.5:1 normal / 3:1 large text.

## Colour, texture, layout
- Practice: No Film School, 60-30-10 colour rule in filmmaking. https://nofilmschool.com/60-30-10-color-rule
- Practice: Boris FX / PremiumBeat on banding; grain/dither over gradients before 8-bit delivery. https://borisfx.com/blog/learn-how-to-handle-banding-in-video/
- Standard (ad spec): Meta Reels safe margins 14% top, 35% bottom, 6% sides, as compiled by Socialync (read 2026-10-11 by that page). https://www.socialync.io/tools/safe-zones
- Practice: Artlist on eye trace and Murch's rule of six. https://artlist.io/blog/eye-trace-and-rule-of-six-editing/
- Practice: frame.io, lower thirds that don't suck — only when it adds value, consistent, brief. https://blog.frame.io/?p=3992

## AI assets
- Practice: Artlist, Genra, Invideo on blending AI b-roll — neutralise then grade, add grain/softness, keep clips short. https://artlist.io/blog/ai-b-roll/
- Practice: Online Tech Tips and others on AI image tells (hands interacting with objects, teeth/eyes, digital sheen). https://www.online-tech-tips.com/how-to-spot-fake-ai-images/

## Sound
- Practice: Sonilo / Krotos on SFX overuse — same whoosh on every cut is a tell, delete 30-50%, align transients to the hit. https://sonilo.com/ai-music/ding-sound-effect-guide

## Observed (our drafts)
- projects/img2442-fresh/src: ~25 distinct hex values incl. #FF2BD6, #22D3A0, #FFE600; 10+ different box-shadows; repeating-linear-gradient stripes; glow; bounce/overshoot/spring; Inter Tight 900 throughout.
- out/IMG_2442-edited-v12.mp4 stills: glossy 3D emoji icons, generic avatars, three left-border cards, pastel blobs, multiple accent colours.
- VJ loves both videos (2026-10-26): keep structure/energy, refine the craft.
