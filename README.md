# Claude Video Studio

Edit videos by talking to Claude Code. This repo is a ready-to-use **studio for Windows**: Claude's instructions, editing and design skills, render scripts and a one-command installer. It contains **no videos, images, models or personal footage** - those stay on your PC.

You give Claude a recording and a goal. Claude watches the footage, decides who it is for, plans the story, cuts it, grades the colour, designs the on-screen text and graphics (without the generic "AI look"), mixes sound, renders a versioned draft and checks the exact file.

> This repository is currently **private**. To let someone use it, add them as a collaborator, or make it public in the repo's Settings. Your recordings are never in this repository either way.

## Install (about 15 minutes, mostly downloads)

Needs Windows 10/11 and an internet connection. A Claude account is needed to sign in to Claude Code. An NVIDIA GPU is optional (faster export and colour); everything also runs on the CPU.

```powershell
git clone https://github.com/Joseph-VJ/claude-video-studio.git C:\VideoStudio
cd C:\VideoStudio
.\Install-Studio.ps1 -InstallPrerequisites
```

`-InstallPrerequisites` uses winget to add anything missing (Git, Node.js LTS, Python 3.12, FFmpeg, Chrome, PowerShell 7). Without it, the installer tells you exactly what to install. If your PowerShell blocks scripts, run once: `Set-ExecutionPolicy -Scope Process Bypass`.

Then install Claude Code if you do not have it (`irm https://claude.ai/install.ps1 | iex`) and start the studio:

```
C:\VideoStudio\Start-DirectorStudio.cmd
```

Claude asks you to sign in the first time. The studio keeps its settings and caches inside its own folder.

## Make your first video

1. Copy a recording into `C:\VideoStudio\raw\`.
2. In the Claude window type, for example:

```
/video-director Edit raw\my-video.mp4 into a clear Instagram Reel for [who it is for]. Inspect the footage first, make a plan, then a versioned draft.
```

Add `PLAN ONLY` to stop after the plan. Finished videos land in `out\`.

| Command | Use it for |
|---|---|
| `/video-director` | Plan and make a full edit (audience, story, cuts, colour, motion, sound) |
| `/video-design` | Design text, captions, cards, icons and motion so they do not look AI-generated; audits the rendered frames |
| `/video-render-fast` | Fast colour + cut render and one deliberate upload export |
| `/video-edit-simple` | Simple edit through the free247editor / Herk kit |
| `/concat-edit` | Editable timeline through the optional Concat app |
| `/request-video-assets` | Claude writes copy-ready prompts when it needs an AI image or clip; you generate it yourself |
| `/remove-background`, `/gemini-clean-assets` | Prepare returned assets |
| `/studio-context` | Save and resume project notes |
| `/video-studio-check` | Diagnose the install |

No paid generation, publishing or upload happens unless you ask. Your recordings are never sent anywhere by the studio.

## What gets installed where

| Folder | Content | In git? |
|---|---|---|
| `CLAUDE.md`, `plans\`, `my-style\`, `.claude\` | Instructions, workflows, skills, commands | yes |
| `scripts\`, `projects\renderer\` | Render, export, audit and context tools; Remotion graphics project | yes |
| `raw\`, `out\`, `work\`, `projects\<yours>` | Your footage, renders and edits | **never** |
| `.venv\`, `models\`, `tools\`, `cache\`, `repos\`, `.agents\` | Installed by the installer | no |

Models (about 20 MB) are downloaded and hash-checked by `scripts\Download-Models.ps1`; speech models download on first transcription.

## Options

```powershell
.\Install-Studio.ps1 -Gpu                 # NVIDIA: CUDA libraries for transcription and CuPy for GPU colour
.\Install-Studio.ps1 -SkipModels          # skip the model downloads
.\Install-Studio.ps1 -SkipThirdParty      # skip the upstream editing kits
.\Install-Studio.ps1 -CheckOnly           # report what is missing, change nothing
.\scripts\Test-Install.ps1                # re-run the self test
.\Update-Studio.ps1                       # pull the latest studio and re-apply your folder paths
```

## Notes

- Windows only. Built and measured on a Ryzen 5 3500 / GTX 1650 PC; speeds in `plans\` are from that machine.
- The studio was written at `E:\Video`. The installer rewrites those paths to the folder you cloned into (`scripts\studio-portable.py`; `Update-Studio.ps1` reverses and re-applies it so `git pull` stays clean).
- Upstream kits (free247editor, Herk Edit Kit, video-agent-skills, video-edit-skill) are fetched from their own repositories at pinned versions, not copied here. See `THIRD_PARTY.md`.
- Start with `CLAUDE.md` and `plans\CLAUDE-FILE-MAP.md` to see how Claude decides what to read for each stage.
- A synthetic encoder test is `scripts\Render-Test.ps1`. The self test checks installation, not creative quality.
- Contributions: edit the instructions in `plans\` and the skills in `.claude\skills\`, test on your own footage, and open a pull request. Never commit footage.
