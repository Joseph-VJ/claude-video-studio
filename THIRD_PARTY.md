# Third-party code, skills and models

This repository only contains files written for this studio, plus the items marked "bundled" below. Everything else is downloaded by `Install-Studio.ps1` from its own upstream, at the pinned commit in `scripts/third-party.json`, so you receive it under its original licence and terms.

| Component | Source | Licence | How it is used here |
|---|---|---|---|
| HyperFrames skills (`hyperframes`, `-animation`, `-cli`, `-core`) | github.com/heygen-com/hyperframes | Apache-2.0 | **Bundled** in `third_party/hyperframes-skills/` with `LICENSE`; copied into `.agents/skills/` at install |
| Image / video prompting skills (`/image`, `/video`) | github.com/smixs/visual-skills by Serge Shima | CC BY 4.0 | **Bundled** in `.claude/skills/image` and `.claude/skills/video` with `LICENSE` and `NOTICE`; adapted for manual generation |
| video-agent-skills (`short-editing`, `vox`, `steal`, `clips`, `broll`, ...) | github.com/Melvynx/video-agent-skills | MIT | Fetched at install |
| free247editor | github.com/riecodes/free247editor | MIT | Fetched at install |
| Herk Edit Kit | github.com/nateherkai/herk-edit-kit | no licence stated | Fetched at install by free247editor's own setup; never redistributed here |
| video-edit-skill (`/video-edit`) | github.com/tenfoldmarc/video-edit-skill | no licence stated | Fetched at install for your own use; never redistributed here |
| Robust Video Matting model | github.com/PeterL1n/RobustVideoMatting | GPL-3.0 | Downloaded at install (hash-checked); not stored in this repository |
| U2-Net small model | github.com/xuebinqin/U-2-Net via github.com/danielgatis/rembg | Apache-2.0 | Downloaded at install (hash-checked) |
| Remotion | remotion.dev | Remotion licence (free for individuals and small companies; check remotion.pro/license for your use) | Installed with npm |
| FFmpeg, Python packages, Node.js, Chrome | their vendors | various | Installed with winget / pip / npm; not stored here |

Remotion has its own commercial licensing terms for companies. Check them before using the Remotion route in a business.

If you are an upstream author and want an item removed or changed, open an issue.
