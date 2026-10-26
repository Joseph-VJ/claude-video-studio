# Video Studio — Installation Result

> Dated installation record: the setup/test facts below describe their original date. Current render operations, known browser limitations, GPU colour/NVENC paths and cache rules are in [FAST-RENDER-WORKFLOW-v1.md](FAST-RENDER-WORKFLOW-v1.md). Use [CLAUDE-FILE-MAP.md](CLAUDE-FILE-MAP.md) for current entry points. Old sign-in/tool test snapshots are not a fresh status check.

Prepared for VJ · 24 October 2026 (India)

## Result

The selected local editing stack is installed and its supported synthetic workflow passed. Claude Code's dedicated studio profile still requires the user's sign-in. No paid Claude inference, real-footage creative edit, publication or source-media upload was performed.

## Installed and connected, in order

| Component | State | Location / version |
|---|---|---|
| Existing core tools | Reused | Claude Code 2.1.308; Node 24.8.0; Python 3.12.13; FFmpeg 8.1 |
| Director/content/audience plan | Installed and referenced by CLAUDE.md and commands | plans/CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md |
| free247editor | Installed | repos/free247editor; commit 86bb088d08c6209c6b427385fe363c8110de3b5b |
| Herk Edit Kit | Installed with pinned dependencies; fresh HyperFrames test rendered | repos/free247editor/kit; commit 10511e5af86fc47756ea89803b397422e2d89284; HyperFrames 0.7.109 |
| Local transcription | Adapter installed; known synthetic text matched | faster-whisper 1.2.1; shared small model tested; existing medium/large-v3 model files reused |
| Existing graphics engine | Reused with a verified compatibility finishing route | Remotion 4.0.537; existing separate HyperFrames 0.8.183 retained |
| Concat | Portable extraction of checksum-verified official MSI; no installer actions executed | tools/Concat-0.2.8/concat.exe |
| Concat MCP | Registered to Claude Code for E:/Video; health check connected | 42 tools; native executable, --mcp headless; writes restricted to E:/Video |
| Launch, diagnosis, rendering and delivery scripts | Installed and syntax checked | Start-DirectorStudio.cmd/.ps1; Start-Concat.cmd/.ps1; scripts/ |

The initial unattended Concat installer action was blocked by the execution policy. The successful alternative extracted the official MSI's files using lessmsi 2.12.9; it did not run Windows Installer or package installation actions.

## What the agent now reads

E:/Video/CLAUDE.md routes editing requests through the director plan and the current style/feedback. It explicitly stops importing the revoked older AGENTS.md instructions. The previous CLAUDE.md is backed up in logs/installation-20261024/CLAUDE.before.md.

The director plan covers content analysis, audience assumptions, creative direction, story and promise/payoff, complete take selection, source-to-output timing, captions, motion, colour, sound, review, revisions and experiments. All 15 requested psychology/strategy/philosophy concepts are present with practical uses and evidence limits. They are planning inputs, not additional software packages or retention guarantees.

Current commands:

- /video-director — understand footage, plan and edit within the requested scope.
- /video-director PLAN ONLY ... — analyse and plan before rendering.
- /video-edit-simple — use the installed free247editor/Herk route.
- /free247editor — alias for the simple workflow.
- /concat-edit — use the editable Concat route.
- /video-studio-check — inspect the installed runtime.

## Start using it

Double-click E:/Video/Start-DirectorStudio.cmd, or run in PowerShell:

    & 'E:\Video\Start-DirectorStudio.ps1'

Sign in once when Claude asks. Put footage in E:/Video/raw and give an exact path plus the audience and intended result. Example:

    /video-director Edit E:/Video/raw/my-video.mp4 into a clear Reel. Understand the message and viewer, plan the story, protect natural skin colour, and add useful speech-timed graphics.

The current Claude sign-in check reported loggedIn=false for the dedicated E:/Video/cache/claude profile. No credential was copied and no account or subscription was purchased. Existing credentials elsewhere were not inspected.

Open the optional timeline app with E:/Video/Start-Concat.cmd. The MCP edits its own projects, rather than promising live changes to the currently visible timeline. Project folder locks apply.

## Fresh verification evidence

| Check | Observed result |
|---|---|
| Herk/free247 setup | Official setup completed and rendered its new 8-second synthetic starter |
| Local word timings | Matched all 10 known words: This is a local video editing test. Every word matters. |
| Director graphics export | 8 seconds, 240 decoded frames, 1080×1920, 30 fps, H.264/yuv420p and AAC |
| Director delivered loudness | -14.04 LUFS integrated; -2.88 dBTP |
| Concat create/import/edit/save | Passed using a new synthetic project, image, audio and title |
| Concat preview and exposure effect | Native GPU preview rendered; a +0.25-stop test adjustment changed pixel values |
| Concat export | 5 seconds, 150 decoded frames, 1080×1920, 30 fps, H.264/yuv420p and AAC |
| Concat delivered loudness | -14.12 LUFS integrated; -3.61 dBTP |
| Concat colour preservation | Maximum sampled decoded RGB difference: 2 levels versus its graded preview |
| Remotion/FFmpeg colour preservation | Maximum sampled decoded RGB difference: 3 levels versus the graded PNG |
| Picture during audio mastering | Decoded picture hashes unchanged for both selected deliveries |
| Technical decode | Both selected files fully decoded without errors |
| Visual samples | Eight exact frames inspected, including both sides of cuts at frames 75 and 150; a full-resolution caption frame and Concat export frame inspected |
| Claude MCP connection | Connected through the native Concat executable with E: config/data paths |

These are synthetic signal/path checks. They do not certify real skin tone, phone HDR interpretation, moving masks, creative take selection or viewer retention. Perceptual full-audio listening was not performed; audio evidence is based on known synthetic speech, transcription, decoding and signal measurements.

## Important Windows compatibility fixes

The installed Remotion package's bundled ffprobe crashes on this PC. Reusing the working system FFmpeg/ffprobe resolves probing, but that FFmpeg does not include libfdk_aac. Direct Remotion AAC encoding is therefore not the supported path.

The working custom-graphics route is scripts/Render-DirectorProject.ps1:

1. Render muted PNG frames with the installed Remotion engine and shared Chrome.
2. Assemble the pictures with the working local FFmpeg and a supplied lossless dialogue/mix track.
3. Encode H.264 once; keep intermediate audio lossless.
4. Use scripts/master-delivery.py to master only audio and copy the video stream.
5. Verify the actual delivered file.

The separate master-delivery.py also handles Matroska duration metadata. Its default speech compression follows the earlier studio mastering settings; --no-compress is available when appropriate. A successful render is not an automatic human approval of its sound.

The legacy scripts/master.py and original renderer sources remain in place. Do not use direct Remotion AAC commands for new projects until compatible binaries are independently verified. The HyperFrames and Concat routes were tested separately.

## Files to review

- plans/DIRECTOR-STUDIO-QUICK-START.md
- plans/CLAUDE-VIDEO-DIRECTOR-PLAN-v1.md
- logs/installation-20261024/doctor.json
- logs/installation-20261024/verification.json — exact hashes and measurements
- logs/installation-20261024/concat-package-checksum.json
- projects/director-setup-20261024-v1/contact-sheet.png
- out/director-studio-synthetic-v2.mp4 — selected director test
- out/concat-synthetic-mastered-v3.mp4 — selected Concat test
- repos/free247editor/outbox/setup-test.mp4 — Herk/HyperFrames starter

Earlier synthetic attempts are not the certified deliveries; use the selected filenames and hashes in verification.json.

## Deliberately not added

Cooked, Lumen, Resolve, Premiere and Shotcut would duplicate the selected main routes. They were not required to complete this installation. No additional large speech model, paid media service or cloud transcription account was added. Existing tenfoldmarc/Melvyn workflows remain available.

## Repositories and helper provenance

- https://github.com/riecodes/free247editor
- https://github.com/nateherkai/herk-edit-kit
- https://github.com/jub0t/Concat/releases/tag/v0.2.8
- https://github.com/activescott/lessmsi/releases/tag/v2.12.9

The companion archive contains the new configuration/commands/scripts, the director plan, installation records and selected synthetic outputs. It excludes credentials, personal style history, original recordings, node_modules, model files and application binaries. It is a setup record and reproducibility aid, not a complete offline installer.
