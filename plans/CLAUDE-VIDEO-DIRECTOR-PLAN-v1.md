# Claude Video Director — Content, Audience and Edit Plan



Version 1.0 · Prepared for VJ · 24 October 2026 (India)



Current render integration (2026-10-25): read FAST-RENDER-WORKFLOW-v1.md for current hardware/tool paths, recipes, caches and exact-output QA; CLAUDE-FILE-MAP.md indexes the rest. Historic setup commands do not override it.



## 1. Purpose and how to use this file



Give this file to Claude Code with your footage folder, available references and the result you want. It is a reusable operating plan, output template and review checklist. It is not an installed editor, an executable renderer or evidence that any footage has been watched. No new recording was supplied or analysed while this file was prepared.



The aim is to make a video worth finishing: understand its meaning, identify the people it can help, choose an honest story, shape the performance, explain visually, preserve natural colour, mix clear sound and inspect the delivered result.



One agent can perform all the roles below sequentially. Multiple agents, multiple editors and paid services are not required by this plan. Follow applicable system, user and workspace instructions; this file does not override them. Previously revoked workspace rules must not be silently reinstated.



### Copy this starting request into Claude



```text

Read E:/Video/plans/CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md and use it for this project.



Footage: [folder or attached files]

Audience, if known: [people and their situation]

Goal: [explain / earn trust / demonstrate / generate qualified enquiries / other]

Platform: [Instagram Reel / YouTube Short / other]

References, if supplied: [files or links]

Known facts and pronunciation: [names, terms, important figures]

My constraints and preferences: [anything already decided]

Mode: [PLAN ONLY / MAKE A DRAFT]



For each new recording, start its content and colour decisions fresh. Do not

copy the previous video grade, LUT, mask, white balance, cuts or graphics.

Continue an existing edit with its own approved treatment. Before rendering

read FAST-RENDER-WORKFLOW-v1.md and maintain Project/.context/RENDER.md.



First inspect the actual footage and sound. Explain the content in plain

language, identify the viewer's problem, and distinguish observed evidence

from audience assumptions. Use the roles and output format in this file.



Plan the story, cuts, captions, motion, colour and sound around the content.

Consider the 15 concepts in section 5, select only useful ones and explain

their practical purpose. Treat neuroscience, strategy and personal philosophy

as different kinds of evidence. Do not promise a retention rate.



Reuse one suitable installed editing route. Keep the source-to-output map,

preserve complete meaning, and keep colour correction explicit. If Mode is

MAKE A DRAFT, save the plan and continue to a versioned preview and QA within

my authorised scope. If Mode is PLAN ONLY, deliver the plan and stop before

rendering. If mode is missing, analyse and plan first; do not assume a software

installation or publication request.



Ask only about missing information that materially prevents a good decision.

Otherwise state a reasonable assumption and keep working. Never describe

contact sheets or a transcript as full continuous audiovisual review.

```



## 2. The roles Claude must perform



These are responsibilities, not claims to professional credentials. Each role must leave a concrete decision that the next role can use.



| Role | Main questions | Required output |

|---|---|---|

| Content analyst | What was actually said and shown? What is the central argument? | Corrected transcript, content summary, claim/evidence list and uncertainties |

| Audience researcher | Who has this problem, in what situation, and with what prior knowledge? | One primary viewer profile, viewer question, objections and labelled hypotheses |

| Creative director | What should this video accomplish and what treatment fits it? | One-sentence promise, tone, visual direction and success criteria |

| Film director | Which performance communicates the idea most clearly? Where should we stay with the face? | Selected performances, emotional progression, framing and continuity notes |

| Story editor | What order gives the viewer a reason to continue and a satisfying answer? | Story spine, useful opening, setup, demonstration, payoff and ending |

| Precision editor | Which exact source ranges stay, and where are natural joins? | Editable EDL, removed-range reasons, word anchors and source-to-output mapping |

| Motion designer and caption editor | What needs to be shown, labelled or animated to make it understandable? Does it look designed for this speaker rather than like an AI template? | Speech-anchored graphics, text hierarchy, caption policy, layout checks and the project's `.context/DESIGN.md` (use `/video-design`) |

| Colourist | Is the footage interpreted correctly? Are exposure, complexion and shots consistent? | Technical colour path, shot corrections, creative look and comparison frames |

| Sound designer | Can every word be heard? What does music or an effect add? | Voice treatment, meaningful cues, ducking and delivered loudness measurements |

| Delivery and review editor | Does the actual export match the plan? What remains unverified? | Versioned output, editable project, exact-file QA and honest review status |

| Experiment analyst | Where did viewers leave, misunderstand or take action? | Post-release hypotheses and controlled revisions when analytics are supplied |



Resolve conflicts in this order: accurate meaning and evidence; comprehension and accessibility; natural performance and colour; audience relevance and promise fulfilment; then decorative motion and novelty. A strong effect cannot rescue an unsupported claim.



## 3. Inspect and understand before designing



### 3.1 Inventory the real material



1. List sources and record file identities, durations, codecs, rotation, frame timing, audio channels and colour metadata. Use stable source IDs; keep originals intact and create versioned outputs.

2. Identify the available tools through read-only capability checks. Record which capabilities are actually tested, merely documented or unavailable. A visible editor feature does not establish that its MCP interface exposes it.

3. Generate a word-timed transcript with source ID, word ID, start and end. Correct names, numbers, negations, qualifiers and domain terms against the audio. Keep uncertain phrases marked instead of silently guessing.

4. Review all dialogue in source order where audio playback is available. Inspect visual coverage across the complete recording and denser windows around retakes, demonstrations, important gestures, exposure changes and candidate cuts. Use lower-resolution proxies for exploration where helpful; validate final crops from originals.

5. Review motion and audiovisual joins around every planned cut. Stills cannot establish a smooth gesture or an unclipped spoken join.

6. If continuous playback or audio assessment is unavailable, document that limitation and the exact coverage achieved. Do not say you watched or heard everything on the strength of samples or ASR alone.

7. Record clipped highlights, noise, flicker, rolling shutter, focus failures, mixed light and other issues. Separate repairable problems from missing source information.



### 3.2 Produce the content model



Fill these fields before picking a look:



| Field | Required answer |

|---|---|

| Literal topic | What this recording discusses, without a new marketing angle |

| Main message | One sentence that the retained footage genuinely supports |

| Viewer problem | The specific situation or decision the video can help with |

| Mechanism | Why the problem happens or how the demonstrated solution works |

| Available proof | Real demonstration, example, comparison, document or supplied evidence |

| Important qualification | Conditions, uncertainty or limitations that must survive the edit |

| Desired change | What the viewer should understand or be able to do afterwards |

| Missing material | Unrecorded explanation, proof, transition, shot or reshoot needed |

| Best performances | Complete take options, with reasons beyond simply picking the last one |



Do not infer that a business has a particular audience, conversion problem or future product solely because it would make a stronger story. Mark it as a hypothesis unless the footage or supplied brief supports it. Verify external factual claims when needed; an edited speaker assertion is not independent proof.



### 3.3 Build one primary viewer profile



Describe a situation rather than inventing a demographic persona:



- They are trying to: [specific task or outcome].

- They already know: [likely prior knowledge, with confidence].

- They are confused by: [one principal gap].

- They may object: [plausible objection and supporting evidence, if any].

- They might skip because: [irrelevance, repetition, vagueness, unreadable detail, weak proof, confusion or another labelled hypothesis].

- They should finish thinking: [useful takeaway].

- The appropriate next action is: [one proportionate action or none].

- Evidence basis: [recorded content / supplied audience data / previous analytics / assumption].



Language, literacy, screen size, sound-off viewing and domain familiarity affect the treatment. Ask about language or caption spelling when the answer changes the deliverable. Do not assume every Tamil recording needs English translation or Romanised Tamil captions.



## 4. Build the story around a useful promise



### 4.1 Choose a story form that fits the material



| Material | Useful structure | What makes it worth finishing |

|---|---|---|

| Explanation | Question → mechanism → example → usable answer | Understanding improves at each step |

| Problem and solution | Recognisable situation → cause → practical fix → limits | Viewer sees what to do and why |

| Demonstration | Outcome glimpse → process → actual result → caveat | The result is shown, not merely promised |

| Comparison | Decision → common criteria → evidence for options → conditional choice | Viewer can make their own decision |

| Personal story | Situation → obstacle → meaningful choice → consequence → reflection | A truthful change with earned emotion |

| Service or product | Specific need → fit → working example → qualification → next step | Viewer can judge whether it suits them |

| News or update | Verified change → who it affects → implications → uncertainty | Timely explanation with clear attribution |



Do not impose problem-agitation-sales structure on a reflective story or an explanation that needs a calm demonstration.



### 4.2 Design a truthful opening



Propose at most three viable openings from the available footage. Label each as an existing recorded line, a faithful rearrangement, new on-screen editorial text or a reshoot request. Never invent dialogue or represent generated speech as the original performance.



Each opening needs:



1. A specific person or situation it is relevant to.

2. A clear promise the actual video can fulfil.

3. A source-supported question, demonstration, contrast or observation.

4. A credible route to the answer.



Begin with useful information as early as the delivery allows. The first seconds are a creative decision, not a biologically fixed three-second rule. Avoid empty greetings when they delay the point; preserve introductions when context or trust needs them.



### 4.3 Manage curiosity and payoff



Use a small number of understandable unanswered questions. Record each opening promise in a promise ledger:



| Promise ID | Exact question or expectation | Where opened | What constitutes an answer | Where answered | Source evidence |

|---|---|---|---|---|---|



Give useful answers during the video. Do not indefinitely postpone basic information to force a finish. Resolve the main promise before an optional CTA. If the source cannot pay off the hook, change the hook or flag the missing explanation.



### 4.4 Plan an emotional progression



State the intended progression in everyday language: recognition → curiosity → understanding → confidence, for example. These are creative intentions, not measured emotional states. Preserve a sincere performance; do not manufacture distress or certainty through misleading sound, reaction shots or reordered statements.



## 5. The 15 requested concepts: practical use and limits



Use this as a consideration menu. Select only the few concepts that help this video; list the rest as not selected with a short reason. Do not insert the names into captions or narration unless they are the subject of the recording.



Evidence labels:



- **Research topic:** studied phenomenon, with an explicit limit on applying it to editing.

- **Creative heuristic:** a proposed design choice to test with viewers.

- **Strategy:** a business or production lens rather than a brain mechanism.

- **Philosophy/self-help:** an author's framework or belief, not established biological evidence.



| Concept | Classification and evidence boundary | Useful editorial translation | Do not infer or promise |

|---|---|---|---|

| Psycho-Cybernetics | Maxwell Maltz's self-help framework involving self-image and mental rehearsal; its publisher describes those themes. [S09] | When relevant, help the viewer imagine completing a concrete, realistic task. Show an observable process and attainable next step. | That an edit programs the subconscious or proves the framework scientifically. |

| Neuroplasticity | Learning-related neural change is studied; the cited motor-learning experiment involved repeated practice over time, not watching Reels. [S04] | For educational material, teach a manageable action, revisit a useful example and support practice across episodes. | That a single clip rewires the brain, or that a cut rate triggers plasticity. |

| Default Mode Network | A neuroscientific research topic; the foundational study is not a video-retention recipe. [S03] | No default edit prescription. A relevant viewer scenario may be tested for clarity and recognition on ordinary editorial grounds. | That Claude can switch off, suppress or measure a viewer's DMN through an edit. |

| Dopamine Loops | Dopamine reward-prediction-error research exists; applying it to a particular Reel is an untested extrapolation. [S02] | Use honest curiosity → meaningful progress → useful payoff. Describe it as a storytelling hypothesis. | Dopamine spikes, addiction engineering, universal timing rules or guaranteed completion. |

| Attention Residue | Studied in switching between work tasks, not as a direct test of caption transitions. [S05] | Keep subject changes clear, complete a comparison before introducing another and avoid competing unrelated tasks on screen. | A measured reduction in attention residue or a proven Reel-retention effect. |

| Flow State | An established psychological concept used here only as a creative analogy; no direct flow evidence is claimed for this system. | Aim for understandable challenge, coherent progression and pacing appropriate to the audience. | That watching a short video enters a measurable flow state. |

| Hedonic Treadmill | Adaptation is a research topic; it does not establish a need for faster editing. No direct retention result is claimed here. | Avoid repeating the same meaningless flourish. Vary useful presentation and allow calmer moments. | That increasingly intense effects prevent adaptation or improve learning. |

| Game Theory | A formal field concerning strategic interaction; no game-theoretic model of this audience is supplied. | Use a simple alignment lens: the creator earns attention by helping the viewer. Make value and conditions clear. | That viewers are opponents to defeat, or that a generic game theory label validates persuasion. |

| Asymmetric Bets | A strategy lens with no claim of scientific editing validation. | Test low-cost openings or one graphic treatment while protecting the main message and quality. | Guaranteed upside, imaginary probabilities or investment advice. |

| Naval Ravikant | A person's published business ideas, including leverage; attribution is not proof of a retention effect. [S08] | Use distinctive domain knowledge, clear explanations and reusable production assets where they suit the brief. | That imitation of his style guarantees influence, income or authority. |

| Permissionless Leverage | A strategy described in Naval's discussion of code and media. [S08] | Create reusable motion components, a pronunciation dictionary, templates and an organised project that make later work cheaper. | That reuse replaces source verification or removes platform/licensing constraints. |

| Escaping the Default Game | A broad framing idea; no single scientific definition is assumed. | Where supported, question an unhelpful assumption and demonstrate a credible alternative. | Invented contrarian claims or the assertion that the mainstream choice is always wrong. |

| Value Maxing | Working definition for this plan: useful understanding per unit of viewer time. This is a project heuristic, not a validated score. | Remove repetition; keep demonstrations, important qualifications and actionable explanation. | That maximum speed, word count or effects equal maximum value. |

| Ideas → Influence | Communication strategy rather than a neural mechanism. | Make the central idea clear, credible, memorable and easy to apply or explain to someone else. | That memorability establishes truth or that influence is guaranteed. |

| Neville Goddard | Spiritual/self-help writing about imagination and assumed outcomes. The cited original work is consulted as philosophy, not experimental evidence. [S10] | If relevant to the creator's message, use a clearly hypothetical imagined future or visualised goal, paired with concrete action. | Manifestation as a scientific result, fabricated success evidence or belief alone guaranteeing outcomes. |



### 5.1 Additional principles worth including



These are more directly useful to production than applying every fashionable term:



| Principle | Practical decision | Evidence boundary |

|---|---|---|

| Coherence | Remove irrelevant detail and decorative inserts that compete with explanation. | Multimedia-learning research concerns learning, not an Instagram completion-rate guarantee. [S01][S07] |

| Signalling | Highlight the exact part of a diagram or demonstration being discussed. | Use it to clarify; verify readability and comprehension in this context. [S01] |

| Visual/verbal alignment | Show the matching object, step or comparison when the relevant words occur. | Same cited multimedia-learning boundary; avoid overload from competing text. [S01] |

| Event continuity | Cut at understandable changes in action or thought and preserve meaningful continuity. | A narrative-film study supports the relevance of continuity to event perception, not a universal cut interval. [S06] |

| Information gap | Frame a specific question whose answer genuinely matters and is provided. | Curiosity theory informs a hypothesis; it does not guarantee watch time. [S11] |

| Proof and specificity | Prefer a real example to a vague benefit claim. Label demonstrations and illustrations honestly. | Editorial practice; assess truth and audience understanding separately from retention. |

| Reading and processing time | Hold a diagram, qualification or number long enough to be understood on a phone. | Check the actual language, text length, device and target viewers. No universal words-per-second target is assumed. |

| Accessibility | Keep dialogue clear, captions readable, face unobstructed and motion restrained where necessary. | Evaluate the actual output; a safe rectangle alone does not prove accessibility. |



## 6. The complete planning workflow



### Pass A — meaning and audience



Write the content model and viewer profile. Identify ambiguities and unsupported claims. Give an evidence basis and confidence to important assumptions. If the video has several unrelated messages, propose separate edits rather than force all of them into one hook.



### Pass B — story and spoken edit



Select complete takes for accuracy, delivery, eye contact, gesture and continuity. Preserve useful breaths and emphasis. Remove fillers only where removal is clean and does not distort tone. A transcript that omits a false start is not evidence that the false start did not happen.



Do not apply another silence-removal pass after timing graphics. Changes to retained ranges require a new timing revision and regeneration of dependent captions and cues.



### Pass C — colour sample and renderer check



Because colour is a stated priority, establish representative exposure and colour correction early. Test one graded shot through the chosen compositor and final encode before investing in dense graphics. This proves a specific processing path, not the whole recording.



### Pass D — direct the visual treatment



For each beat, choose the most useful treatment: face, demonstration, supplied B-roll, comparison card, diagram, document close-up, screen capture or a deliberate hold. State what the viewer learns from the choice.



A punch-in needs an emphasis or continuity reason. Do not zoom on every stressed word. Keep crop changes within the available image quality and check face clearance at the tightest frame.

Before any graphic is built, run `/video-design`: write the project's `.context/DESIGN.md` from graded stills of this footage (palette sampled from the scene with one accent, one or two type families, one card/shadow style, one icon system, one motion grammar, a "never in this video" list) and review it against the skill's anti-AI-tells list. Defaults nobody chose (indigo/neon colours, glow, glass cards, stripe gradients, emoji clip-art, a new label style per scene, bounce on everything) are what make an edit read as AI-made.



### Pass E — animate, caption and mix



Anchor motion and sound to retained speech and meaningful visual events. Give each beat one dominant point of attention. Use supporting layers only when they are readable together. Keep important spoken explanation audible while graphics are being processed. Keep every design value in one token object in code and follow the DESIGN.md motion grammar (eased entrances on the stressed syllable, shorter exits, no default bounce/elastic).



### Pass F — render and inspect



Use FAST-RENDER-WORKFLOW-v1.md for the exact supported commands. Prefer native frame-accurate footage, cache matching current-job stages, and perform one deliberate delivery encode. Record the encoder and any explicit fallback. Render a versioned draft from the canonical project. Review exported motion, audio, captions and colour. Correct actual problems and record unverified properties. Do not certify the file from a preview of another version.



### Pass G — revise and learn



Turn plain-English notes into scoped changes. Distinguish one-video choices from lasting preferences. Use supplied analytics to generate hypotheses, then compare fair variants; do not retrofit a neuroscience explanation to every increase or drop.



## 7. Required timeline and motion plan



Every output beat must have a row. Split a row if the meaning, source range, layout or colour setup changes materially.



| Beat ID | Output in/out | Source ID and in/out | Retained words / word IDs | Viewer question or need | Story purpose | Visual and framing | Caption/text | Motion cue and duration | Sound cue | Colour setup | Why this helps | Check |

|---|---|---|---|---|---|---|---|---|---|---|---|---|



Use actual source anchors once footage exists. Until then, mark timing as TBC or illustrative. Do not fabricate source timecodes to make a proposal look executable.



### 7.1 Timing contract



- Store one canonical cut and time map. Distinguish source time, edited output time, frame number and caption word identity.

- Define source intervals as start-inclusive/end-exclusive and document their units. Retain rational frame rates; resample delivery explicitly when required.

- For a constant-speed retained segment, `output_time = segment_output_start + (source_time - segment_source_start) / speed`. A speed of 1 means unchanged playback speed. Speed ramps need an integrated time map, not this constant-speed shortcut.

- A word or cue must belong to a retained interval. A word crossing a cut must be reviewed; never silently squeeze it into a different location.

- Derive output frame boundaries from the time map with a declared rounding policy. Avoid accumulated per-clip rounding drift.

- Record any audio fades or overlaps separately. They must not truncate phonemes or create double speech. Review seams in motion and audio.

- When the cut changes, invalidate and regenerate dependent captions, graphics and verification. A grade-only revision should preserve the approved timing.



### 7.2 Motion design rules



For each graphic, specify: semantic purpose, exact words that motivate it, start anchor, settle/hold/exit, position, safe-area bounds, face-clearance test, asset provenance and fallback if unavailable.



Prefer suitable visual grammar:



| Spoken idea | Useful visual |

|---|---|

| A process | A few steps revealed in the same order as the explanation |

| Two choices | Comparable cards with the same criteria and scale |

| A quantity or change | A clearly labelled counter or chart with verified values |

| An objection | A readable question followed by the source-supported answer |

| Software or product use | Actual supplied demonstration or a clearly labelled illustration |

| An abstract mechanism | A simple diagram grounded in the explanation |

| An important human observation | Stay on the face and allow the performance to carry it |



Do not add a visual change every two or three seconds as an unconditional rule. That can be a draft rhythm to test for some material; a diagram, emotional pause or proof may need a longer hold. New visual information should serve the sentence.



### 7.3 Caption policy



Choose explicitly among verbatim captions, lightly cleaned captions, translation, keyword emphasis or no captions. Keep important qualifiers and numbers. If combining verbatim subtitles and emphasis words, maintain a clear hierarchy and one source of caption wording/timing.



Use actual font rendering and the output frame to check wrapping, contrast and script support. Estimate a face-safe region for every crop and test it across motion. Use current platform guidance or confirmed user margins; avoid presenting any rectangle as permanently valid for every app view. Translation accuracy and word timing require separate review.



## 8. Colour correction and grading: a required lane



Colour is part of the plan, not a preset applied at the end. New footage always gets fresh interpretation, correction and mask geometry; previously approved settings belong only to their original edit unless the current user explicitly requests a reference treatment. Never copy the render-speed lab parameters into a new video.



1. **Interpret input.** Probe transfer, primaries, matrix, range, bit depth, HDR side data and capture mode. HEVC, ten-bit and HDR are different properties. Resolve ambiguous interpretation before approving a final look.

2. **Define the path.** Record input interpretation, working representation, tone/gamut mapping if needed, output encoding and where the creative look occurs. Metadata tags alone do not transform pixel values.

3. **Make a neutral correction.** Balance exposure and colour while protecting important detail. Do not assume a bright wall is neutral or allow it to dominate face exposure decisions.

4. **Keep natural complexion.** Preserve the speaker's identity, complexion and skin texture. Do not lighten a person to a generic target. A clearly visible face is the goal; orange, grey/chalky, crushed or washed-out skin is a review problem.

5. **Use selective correction when justified.** A fixed feathered window is not tracking. If the subject moves, review mask position, edge behaviour, motion blur and exposure stability. Record unsupported operations rather than claiming they were performed.

6. **Match lighting setups.** Wide and tight crops of the same take normally share one underlying grade. Match real changes in lighting or camera setup; avoid independent auto-grades on every micro-cut.

7. **Separate correction from look.** Keep creative contrast, warmth and saturation adjustable without undoing the neutral correction. A LUT's expected input must match the pipeline.

8. **Protect graphics.** In the normal SDR route, grade live action before captions and brand graphics. Ensure subsequent transforms do not unexpectedly tint text, logos or product colours.

9. **Review temporal behaviour.** Inspect representative frames, exposure changes, masks and each cut in the final video. A good midpoint does not establish consistency across the shot.

10. **Compare the export.** Check decoded final frames against the graded reference under the same interpretation, plus colour metadata and clipping. Record display limitations. Scopes and pixel statistics support judgment; they do not prove an attractive look.



Never silently replace a failed required colour stage with a generic contrast filter. Report the failure and use a documented, reviewed alternative or keep the output explicitly provisional.



## 9. Sound, pacing and delivery



Prioritise intelligible, natural dialogue. Remove noise conservatively and inspect speech artefacts. Avoid continuous effects under every sentence. A sound cue should reinforce a real action, transition, reveal or emphasis. Use supplied or appropriately licensed music/SFX and record their provenance.



Duck music and effects under speech using the actual mix, not only a fixed volume guess. Allow pauses where they help emphasis or understanding. Do not assume faster playback is a retention improvement.



For a conventional SDR vertical Reel, a sensible starting delivery profile is 1080×1920, constant 30 fps, H.264/yuv420p with AAC, subject to the user's current brief and platform requirements. A working audio target can be -14 LUFS integrated with a ceiling of -1.7 dBTP; this is a chosen delivery target, not a universal platform mandate. Measure the delivered file and note cases where short duration or dynamics make a single loudness number insufficient.



Avoid repeated lossy video encodes. Keep an appropriate intermediate for colour and graphics, then plan one final delivery encode where practical. Render low-resolution previews for iteration; perform final checks on the actual full-resolution delivery.



## 10. Lightweight implementation choices



Apply the installed-capability and quality table in FAST-RENDER-WORKFLOW-v1.md first. The table below is a capability/research menu, not a list of installed or automatically approved tools. Choose one main route per project. This plan does not require installing every repository. Capabilities below are based on documentation reviewed in the preceding research; they must be checked against the selected installed version.



| Route | Best use | Keep simple by | Boundary |

|---|---|---|---|

| Existing folder studio or adapted tenfoldmarc workflow | Use an already functioning local workflow | Reuse its runtime, transcription and project structure | Foreground masking and custom inserts can be expensive |

| free247editor | Straightforward inbox → edit request → draft → feedback | Use its wrapper and one pinned engine | Documented author tests are not a benchmark of this PC |

| Herk Edit Kit | Structured cuts, story planning and reusable graphics | Select needed modules and local transcription | It is a toolkit requiring coordinated project state |

| Cooked | Browser-based cut and render review | Reuse its renderer and review page | A local browser UI still needs processing dependencies |

| Concat | Editable desktop timeline controlled through built-in MCP | Use its supported timeline, effects and export tools | Discover actual automation parameters and test colour/captions |

| Shotcut + independent Shotcut MCP | Editable .mlt projects, effects, previews and rendering | Reuse Shotcut's bundled media stack | Bridge/tool versions and available MLT filters matter |

| Lumen | Windows timeline with an agent Copilot/MCP | Enable only needed integrations | Assess its footprint before choosing it for minimal overhead |



HyperFrames or Remotion can supply custom motion when the main route needs it. They are composition engines, not independent proof of take selection, audience understanding or colour correctness. FFmpeg is useful for probing, controlled processing and final QA. Reuse existing compatible dependencies where possible.



For a low-overhead project: use proxies for inspection, cache a source-identified transcript, render a representative colour/motion sample, limit unnecessary layers, avoid whole-video masking unless needed and perform one main finishing path. No numeric speed or RAM advantage is claimed without a controlled test.



When an operation replaces an entire effect chain or settings object, read and preserve unrelated properties. Confirm colour space explicitly when changing video settings. Snapshot versioned project state before destructive structural operations. Do not treat a success response as proof that all intended pixels or words survived.



## 11. Required output Claude must show



Return the following in a clear plan before detailed rendering, and keep the same fields updated as the project develops:



1. **What I understood:** topic, core message and useful viewer outcome.

2. **Who this is for:** one primary audience, situation and evidence/assumptions.

3. **Why they would watch or skip:** specific hypotheses based on this material.

4. **Chosen story and opening:** actual available line/visual, promise and payoff.

5. **Role decisions:** director, editor, motion, colour and sound choices with reasons.

6. **Concept selection:** concepts considered, selected, not selected and evidence limits.

7. **Timeline plan:** the full beat table from section 7 with real anchors when available.

8. **Colour plan:** input/working/output interpretation, corrections, look and tests.

9. **Sound and caption plan:** language, treatment, readable layout, mix and targets.

10. **Implementation route:** one backend, tested capabilities and gaps.

11. **Deliverables and verification:** project files, render revision and exact-file QA status.

12. **Next revision or experiment:** a specific proposed change and how to judge it.



For a simple clip, keep each section short. Do not replace concrete decisions with a long list of psychology words. A compact clear plan is better than a theoretical essay that cannot be rendered.



### 11.1 Project records to keep when executing



Use the renderer's native project plus a small canonical record. Several of these can be sections of one JSON file for a simple edit; separate them only if useful.



```text

project/

  plan.md                 audience, story, roles and current decisions

  project.json            source identities, cut revision and timing map

  transcript.words.json   corrected source words and retained-word mapping

  captions.json           wording, language, timing and placement

  colour.json             interpretation, corrections, look and version

  .context/DESIGN.md      palette, type, surfaces, icon system, motion grammar (/video-design)

  render/                 editable renderer project and referenced assets

  review.md               feedback, changes and unresolved issues

  qa.json                 evidence tied to exact project/render versions

  out/                    versioned drafts and delivery files

```



Preserve original sources and local asset references. Do not create a second competing master timeline inside another skill. A word correction, cut change or grade change must have a traceable revision.



### Render handoff required with the plan

State the exact source and cut revision, current-job grade/matte/geometry, selected tools and output profile, cache dependencies, audio treatment, sample findings and versioned destinations. Link .context/RENDER.md. Include stage timings and exact-file QA as they become available. The measured short benchmarks are not a promised whole-job speedup.

## 12. Illustrative output — no real footage analysed



This example shows the format for a hypothetical service-business recording. The lines below are invented to demonstrate planning. They are not quotes from VJ's footage, and the proposed durations are not executable source timecodes.



**Content:** A business receives enquiries but sometimes replies late. The speaker explains a simple follow-up process.



**Primary viewer:** A small-business owner who already receives enquiries and is unsure why some become inactive. This audience is an assumption for the example.



**Promise:** Explain a simple way to make follow-up visible and accountable. Do not promise that this alone will increase sales.



**Possible recorded opening if present in the actual source:** “Before buying more enquiries, check what happens after one arrives.” Otherwise this is a reshoot or editorial-title proposal.



**Story:** Recognise the problem → show the missed handoff → demonstrate capture/owner/next action → explain the limit → invite one practical check.



| Proposed output window | Viewer need | Visual direction | Motion and sound | Reason | Real source anchor |

|---|---|---|---|---|---|

| About 0–4 s | Is this about my problem? | Stay on the speaker; one short title only if needed | Restrained opening emphasis | Establish relevance quickly | TBC — requires footage |

| About 4–10 s | What goes wrong? | Clearly labelled illustrative enquiry card awaiting a reply | One card enters, then holds; no fabricated customer data | Make the handoff visible | TBC |

| About 10–22 s | What is the process? | Three steps: capture → owner → next action | Reveal each step when it is explained; voice remains dominant | Show a usable mechanism | TBC |

| About 22–29 s | Does that explain everything? | Return to speaker for qualification | Calm hold, no dramatic sting | Preserve nuance: other causes may exist | TBC |

| About 29–35 s | What can I do next? | One concise action: review a few recent enquiries | Resolve diagram; optional quiet ending | Give a proportionate next step and finish the promise | TBC |



**Selected concepts:** Value Maxing for removing repetition; Ideas → Influence for a clear explanation; curiosity/payoff as a creative heuristic; Permissionless Leverage for a reusable process-card component.



**Not selected:** DMN, neuroplasticity and manifestation language because they do not explain this edit. No claim about a viewer's neural activity is needed.



**Colour:** Natural visible face, stable complexion and consistent exposure across the source take and punch-in. Inspect the source's actual colour encoding before choosing a transform.



**Verification:** Source mapping, true qualifications, phone readability, motion/audio joins and final colour comparison remain pending until real footage and a render exist.



## 13. QA: what must be checked before calling an edit finished



| Area | Required check | Status vocabulary |

|---|---|---|

| Source and meaning | Retained words map back to sources; important qualifications and context survive | verified / issue / not checked |

| Spoken joins | Review every cut boundary in audio and motion; check clipped/repeated words and awkward gesture joins | verified / issue / limited coverage |

| Promise | Every major hook or open question has a source-supported payoff | satisfied / missing / revised |

| Claims and illustrations | Important facts checked as appropriate; invented examples clearly labelled | supported / uncertain / illustrative |

| Captions | Wording, names, figures, script, synchronisation, wrapping and face clearance | verified / issue / limited coverage |

| Motion | No unexplained flashes, freezes, unreadable holds, misleading diagrams or missing assets | verified / issue / limited coverage |

| Design | Rendered frames match DESIGN.md; `/video-design` design-audit.py flags reviewed; anti-AI-tells checklist walked on the contact sheet and key stills | pass / issue / not checked |

| Colour | Correct interpretation; reviewed face, shot continuity, mask motion and final-export comparison | verified / issue / limited coverage |

| Audio | Dialogue intelligibility, artefacts, ducking, peaks and delivered loudness | measured / listened / issue / unavailable |

| Technical file | Probe dimensions, frame rate, pixel format and codecs; fully decode the file | pass / fail / not run |

| Revision identity | QA records the exact output hash, file name, project revision and settings | current / stale |

| Viewer experience | Explain why it is worth finishing; optionally test comprehension with target viewers | hypothesis / observed / not tested |



At minimum inspect representative beginning/middle/end frames and every cut boundary; increase sampling for captions, exposure movement and complex motion. Sparse frames do not certify every caption or all motion. Where available, review the entire final video with sound. State remaining coverage limits rather than silently passing them.



Rendered-speech ASR can help locate missing or repeated words but is not an infallible second opinion, particularly if the same model made the original mistake. Review critical names, figures and negations against audio and intended meaning.



The delivery receipt should include source hashes/IDs, plan/cut/grade/caption revisions, renderer/version, chosen settings, output hash, check results and unresolved limitations. A changed output invalidates its former exact-file receipt.



## 14. Plain-English feedback and scoped revisions



Translate a note into observable work:



| Feedback | Change | Preserve unless requested |

|---|---|---|

| “Captions too small” | Adjust font size, wrapping and placement; recheck face and margins | Approved words, cut and grade |

| “Less zoom” | Reduce crop magnitude/frequency and inspect reframing | Dialogue selection, graphic meaning and colour |

| “Warmer face” | Review colour balance and local correction; compare motion and final encode | Approved cut, speed and captions |

| “It feels boring” | Identify a specific relevance, repetition, clarity, proof or pacing issue; propose a focused revision | Accuracy and natural performance |

| “Make it cinematic” | Translate into reference properties: contrast, highlight roll-off, motion, sound or pacing | Visible complexion and supported content |

| “Explain better” | Repair story order or add a source-supported demonstration | Important conditions and facts |



Save the note, interpretation, actual change, output version and verification. Mark preferences as project-only unless the user confirms they should recur. Conflicting notes need a current decision; do not accumulate mutually incompatible defaults.



## 15. Learn from actual viewer data



When analytics become available, record platform, audience/distribution context, duration, observation window and the metric definition. Do not invent percentages or compare unlike definitions.



Useful observations can include early hold where exposed, completion, average watch time, rewatching, saves, qualified enquiries and comments showing comprehension. A rewatch may mean enjoyment or confusion; completion alone does not establish usefulness.



For each drop or improvement:



1. Identify the exact timeline region and what happens there.

2. Propose alternative explanations: audience mismatch, delivery, confusion, weak proof, distribution or sampling variation.

3. Choose one low-cost change, such as an opening, a shorter repeated passage or a clearer demonstration.

4. Keep the rest comparable and record the variant.

5. Treat small or uncontrolled comparisons as directional. Separate a randomised test, if the platform supports one, from an organic before/after comparison.

6. Check comprehension and lead quality where relevant, rather than optimise completion at the expense of the stated goal.



Do not estimate an expected retention lift from psychology labels. The relevant outcome is observed performance in context, with uncertainty.



## 16. Research notes and source boundaries



The research below informs distinctions and hypotheses. None of these papers validates this combined workflow, proves that a particular cut releases dopamine, or predicts a completion rate. Editing translations in this plan are proposed design choices unless explicitly described otherwise. Summaries are paraphrases.



- **[S01] Mayer & Moreno (2003), “Nine Ways to Reduce Cognitive Load in Multimedia Learning.”** Discusses managing overload in multimedia learning. It supports considering limited processing capacity and presentation design; it is not a social-platform retention experiment. [Publisher](https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_6) · [University-hosted paper](https://www.umassmed.edu/globalassets/pediatrics/pediatrics-residency-program/woo-insider/resources/nine-ways-to-reduce-cognitive-load-in-multimedia-learning.pdf)

- **[S02] Schultz (2016), “Dopamine reward prediction error coding.”** Describes dopamine-related prediction-error signalling. It does not supply a formula for hooks or edit intervals. [Author review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4826767/)

- **[S03] Raichle et al. (2001), “A default mode of brain function.”** Foundational work on a baseline pattern of brain activity and task-related changes. It does not test video editing. [Original paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC14647/)

- **[S04] Karni et al. (1995), “Functional MRI evidence for adult motor cortex plasticity during motor skill learning.”** Examines changes associated with repeated motor practice. It does not establish that passive short-video exposure causes the same effects. [Original study abstract](https://pubmed.ncbi.nlm.nih.gov/7675082/)

- **[S05] Leroy (2009), “Why is it so hard to do my work? The challenge of attention residue when switching between work tasks.”** Work-task switching is its domain. Applying its idea to editing is a hypothesis. Publisher full text was unavailable during this pass; identification and scope were checked through search-visible metadata and the researcher's university account. [Publisher record](https://www.sciencedirect.com/science/article/pii/S0749597809000399) · [University account of the research](https://www.uwb.edu/news/2024/05/17/an-ongoing-study-on-the-success-of-staying-focused)

- **[S06] Magliano & Zacks (2011), “The Impact of Continuity Editing in Narrative Film on Event Segmentation.”** Examines how film discontinuities relate to event perception. It supports reviewing meaningful continuity, without specifying a universal editing speed. [Original paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3208769/)

- **[S07] Sundararajan & Adesope (2020), “Keep It Coherent: A Meta-Analysis of the Seductive Details Effect.”** Synthesises learning research concerning interesting but irrelevant additions. Context and moderators matter; learning is not identical to watch time. The abstract and publication record were consulted, not a claim of full-paper replication. [Publication record](https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Keep-it-Coherent-A-Meta-Analysis-of/99900601155501842) · [Abstract](https://eric.ed.gov/?id=EJ1263249)

- **[S08] Naval Ravikant, “How to Get Rich.”** The author's account of business ideas including media/code leverage. Use as attributed strategy, not neuroscience or guaranteed financial results. [Author's site](https://nav.al/rich)

- **[S09] Maxwell Maltz, “Psycho-Cybernetics.”** Publisher descriptions establish its self-image, visualisation and mental-rehearsal themes. They do not independently validate its claims. [Publisher](https://www.hachetteindia.com/Home/bookdetails/Info/9781800812925/psycho-cybernetics-updated-and-expanded)

- **[S10] Neville Goddard, “Feeling Is the Secret” (1944).** Original spiritual/self-help text as reproduced in an archive; not an experiment or neuroscience source. [Archived text](https://thenevillegoddard.com/works/feeling-is-the-secret/)

- **[S11] Loewenstein (1994), “The Psychology of Curiosity: A Review and Reinterpretation.”** Presents an information-gap account of curiosity. An opening/payoff strategy is a proposed application, not a result tested for these videos. [Original paper hosted by the author's university](https://www.cmu.edu/dietrich/sds/docs/loewenstein/PsychofCuriosity.pdf)



### Tool documentation consulted for the implementation shortlist



- [free247editor](https://github.com/riecodes/free247editor)

- [tenfoldmarc/video-edit-skill](https://github.com/tenfoldmarc/video-edit-skill)

- [Herk Edit Kit](https://github.com/nateherkai/herk-edit-kit)

- [Cooked](https://github.com/nextwork-projects/ai-video-editor-cooked)

- [Concat](https://github.com/jub0t/Concat)

- [Shotcut MCP](https://github.com/matrodrigs/shotcut-mcp) and [Shotcut requirements](https://shotcut.org/FAQ/)

- [Lumen](https://github.com/Mas-inx/lumen-ai-video-editor)

- [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html)

- [Remotion colour-space handling](https://www.remotion.dev/docs/options/color-space)



These sources establish documented approaches, not that all repositories have been installed, audited line by line or benchmarked together. The earlier colour-first research remains a companion investigation; this file adds the content/audience/director planning layer and does not overwrite that report.



## 17. Definition of a useful result



The viewer can recognise why the video matters, follow the explanation and receive the promised answer. The performance and claims remain faithful to the source. Graphics explain the current idea. Colour and sound remain consistent through export. Revisions are traceable, and verification says exactly what was checked.



The goal is a clear, credible, engaging video. Full-watch behaviour is something to observe and improve; it cannot be promised for every viewer.

