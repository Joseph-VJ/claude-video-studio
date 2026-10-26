# Manual asset generation
Claude inspects the actual edit and asks only for useful missing assets. It writes assets/requests/ASSET-ID.md, records the timeline anchor and shows the copy-ready prompt in chat.
You generate in your chosen image/video tool and save files under the project's assets/incoming folder with the requested name.
Claude checks returned files, saves processed versions, updates the manifest and replaces the matching placeholder.
No external generation service is connected or called automatically.

## Prompt example: video
Asset: A001, 00:07.2-00:10.2, illustrate attention residue, requested target 9:16 / 1080x1920 / 4 seconds plus short motion handles.
Prompt: Vertical close shot of a person's hands at a clean wooden desk, one open notebook and a face-down phone. The hand reaches toward the phone, pauses, then turns back to underline one line in the notebook. Locked camera, soft window light from frame left, natural warm-neutral colour, realistic skin texture. Keep the notebook position and hand anatomy stable. End on the pen completing the underline with a brief still hold. Quiet room tone only; no speech. Keep the lower quarter visually simple for captions added in editing.
Filename: A001-attention-residue-v1.mp4
Acceptance: clear single action, stable fingers and notebook, no generated text required, stable framing, usable beginning/end.
This is a model-neutral target; confirm supported duration and controls in your selected tool.

## Prompt example: image
Asset: A002, comparison graphic, 9:16 requested target.
Prompt: Create a clean editorial still of two identical clear glasses on a matte charcoal tabletop. The left glass is half full of water and the right is empty. Side light from the upper left, restrained neutral palette, clear separation between glass edges and the background, generous empty space above for labels added in editing. Maintain straight tabletop perspective and realistic reflections.
Filename: A002-two-glasses-v1.png
Acceptance: exactly two glasses, consistent geometry, clean label space, no baked-in words.

## Render integration

Use the current project's beat/cut/colour plan and .context/RENDER.md. Returned generated assets need metadata, frame cadence, colour interpretation, duration/handles, alpha and edge/motion review before compositing. Do not apply the previous recording's grade to a new asset by default. Preserve originals and store source/processed hashes plus tool/settings provenance. Cache accepted processing by that identity. A replacement asset invalidates its affected scene/composite/export/QA, not unchanged ASR or unrelated graded footage. Required missing assets remain explicit placeholders, not a final delivery. Use FAST-RENDER-WORKFLOW-v1.md for native/graphics route selection and one deliberate final encode.
