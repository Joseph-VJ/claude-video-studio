"""Build the shareable studio repository from E:/Video into a clean folder (allowlist only).

Nothing outside ALLOW can ever be copied. Media, models, caches, projects, virtual environments, third-party code with unclear licences,
settings with local permissions and credentials are all left out. Every exported file is scanned: media/binary files and secret-looking
strings abort the export.

  python scripts/export-repo.py --dest E:/claude-video-studio            # copy + scan
  python scripts/export-repo.py --report                                  # what would be exported, sizes, machine paths
"""
import argparse, fnmatch, hashlib, json, os, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_TEMPLATES = ROOT / "repo-template"          # files that exist only in the repo (README, LICENSE, installer, .gitignore ...)

# (source path relative to ROOT, destination relative to repo). A directory is copied recursively, minus EXCLUDE.
ALLOW = [
    ("CLAUDE.md", "CLAUDE.md"),
    ("CLAUDE-CODE-GUIDE.md", "CLAUDE-CODE-GUIDE.md"),
    ("README.md", "docs/studio-overview.md"),
    ("requirements.lock.txt", "requirements.lock.txt"),
    ("Start-DirectorStudio.ps1", "Start-DirectorStudio.ps1"),
    ("Start-DirectorStudio.cmd", "Start-DirectorStudio.cmd"),
    ("Start-ClaudeVideo.ps1", "Start-ClaudeVideo.ps1"),
    ("Start-Concat.ps1", "Start-Concat.ps1"),
    ("Start-Concat.cmd", "Start-Concat.cmd"),
    ("Start-VideoStudio.ps1", "Start-VideoStudio.ps1"),
    ("plans", "plans"),
    ("my-style/style.md", "my-style/style.md"),
    ("my-style/feedback.md", "my-style/feedback.md"),
    (".claude/commands", ".claude/commands"),
    (".claude/skills", ".claude/skills"),
    ("scripts", "scripts"),
    ("projects/renderer", "projects/renderer"),
    ("projects/img2442-fresh/src/kit.tsx", "templates/remotion-design-kit/kit.tsx"),
    ("projects/img2442-fresh/.context/DESIGN.md", "examples/DESIGN.example-img2442.md"),
    (".agents/skills/hyperframes", "third_party/hyperframes-skills/hyperframes"),
    (".agents/skills/hyperframes-animation", "third_party/hyperframes-skills/hyperframes-animation"),
    (".agents/skills/hyperframes-cli", "third_party/hyperframes-skills/hyperframes-cli"),
    (".agents/skills/hyperframes-core", "third_party/hyperframes-skills/hyperframes-core"),
]
EXCLUDE_DIRS = {"node_modules", "__pycache__", ".git", "out", "frames", "dist", "build", ".venv", ".runtime", "cache", ".cache"}
EXCLUDE_PREFIXES = ("projects/renderer/public", "projects/renderer/out", "scripts/__pycache__")
EXCLUDE_GLOBS = ["*.pre-fast-render-*", "*.zip", "*.log", "package-lock.json.bak", ".DS_Store", "Thumbs.db"]
TEXT_EXT = {".md", ".py", ".ps1", ".cmd", ".json", ".txt", ".ts", ".tsx", ".js", ".cjs", ".mjs", ".html", ".css", ".yml", ".yaml", ".toml", ".gitignore", ".gitattributes", ".lock", ".svg", ".example", ""}
MEDIA_EXT = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".heic", ".psd", ".ico", ".exr",
             ".onnx", ".bin", ".pt", ".pth", ".safetensors", ".gguf", ".ttf", ".otf", ".woff", ".woff2", ".exe", ".dll", ".zip", ".7z", ".tar", ".gz", ".msi", ".pyc", ".node"}
SECRET_PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{40,}"), "GitHub fine-grained token"),
    (re.compile(r"sk-[A-Za-z0-9_-]{30,}"), "API key (sk-)"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS key id"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"), "Slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"), "credential assignment"),
]
PII_PATTERNS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "email address"),
    (re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)"), "Indian mobile number"),
    (re.compile(r"C:\\Users\\[A-Za-z0-9_.-]+", re.I), "Windows user profile path"),
]
ALLOWED_EMAILS = {"noreply@anthropic.com"}


def excluded(path: pathlib.Path, base: str = "") -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    rel = (base + "/" + path.as_posix()).strip("/")
    if any(rel == pre or rel.startswith(pre + "/") for pre in EXCLUDE_PREFIXES):
        return True
    return any(fnmatch.fnmatch(path.name, g) for g in EXCLUDE_GLOBS)


def plan():
    items = []
    for src, dst in ALLOW:
        s = ROOT / src
        if not s.exists():
            print(f"WARN missing {src}", file=sys.stderr); continue
        if s.is_file():
            items.append((s, pathlib.PurePosixPath(dst)))
        else:
            for p in sorted(s.rglob("*")):
                rel = p.relative_to(s)
                if p.is_file() and not excluded(rel, src):
                    items.append((p, pathlib.PurePosixPath(dst) / pathlib.PurePosixPath(rel.as_posix())))
    if SRC_TEMPLATES.exists():
        for p in sorted(SRC_TEMPLATES.rglob("*")):
            if p.is_file() and not excluded(p.relative_to(SRC_TEMPLATES)):
                items.append((p, pathlib.PurePosixPath(p.relative_to(SRC_TEMPLATES).as_posix())))
    by_dest = {}
    for s, d in items:
        by_dest[d.as_posix()] = (s, d)          # later entries (repo-template) override earlier ones
    return list(by_dest.values())


# Regex replacements applied to the exported copies so no machine-specific path remains. Each must match at least once, or the export aborts.
CLAUDE_EXE = r"'[A-Za-z]:\\Users\\[^\\']+\\\.local\\bin\\claude\.exe'"
TRANSFORMS = {
    "Start-DirectorStudio.ps1": [(r"&\s+" + CLAUDE_EXE, "& claude")],
    "Start-ClaudeVideo.ps1": [(r"\$claudeExe=" + CLAUDE_EXE, "$claudeExe=(Get-Command claude -ErrorAction Stop).Source")],
    "scripts/Check-DirectorStudio.ps1": [(r"&\s+" + CLAUDE_EXE, "& claude")],
}


def transform(dst: str, text: str) -> str:
    for pattern, new in TRANSFORMS.get(dst, []):
        text, n = re.subn(pattern, lambda m: new, text)
        if n == 0:
            raise SystemExit(f"transform for {dst} did not match: {pattern}")
    return text


def scan(items):
    problems = []
    for src, dst in items:
        ext = src.suffix.lower()
        if ext in MEDIA_EXT:
            problems.append((str(dst), f"media/binary extension {ext}")); continue
        data = src.read_bytes()
        if b"\x00" in data[:4096]:
            problems.append((str(dst), "binary content")); continue
        text = transform(dst.as_posix(), data.decode("utf-8", errors="replace"))
        if ext == ".ps1" and any(ord(c) > 127 for c in text):
            problems.append((str(dst), "non-ASCII in .ps1 (Windows PowerShell 5.1 would misread it)"))
        if ext == ".json":
            try:
                json.loads(text)
            except ValueError as e:
                problems.append((str(dst), f"invalid JSON: {e}"))
        for rx, label in SECRET_PATTERNS:
            if rx.search(text):
                problems.append((str(dst), f"possible secret: {label}"))
        for rx, label in PII_PATTERNS:
            for m in rx.finditer(text):
                if label == "email address" and m.group(0).lower() in ALLOWED_EMAILS:
                    continue
                problems.append((str(dst), f"{label}: {m.group(0)[:40]}"))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--allow-pii", action="store_true", help="export even if PII patterns match (secrets and media still abort)")
    a = ap.parse_args()
    items = plan()
    total = sum(s.stat().st_size for s, _ in items)
    print(f"{len(items)} files, {total / 1e6:.2f} MB")
    problems = scan(items)
    hard = [p for p in problems if p[1].startswith(("media", "binary", "possible secret", "non-ASCII", "invalid JSON"))]
    soft = [p for p in problems if p not in hard]
    for p in hard: print("BLOCK", *p)
    for p in soft[:60]: print("PII  ", *p)
    if len(soft) > 60: print(f"... {len(soft) - 60} more PII hits")
    if a.report or not a.dest:
        return 1 if hard else 0
    if hard or (soft and not a.allow_pii):
        print("Export aborted: fix or review the hits above (use --allow-pii only after reviewing every PII hit)."); return 2
    dest = pathlib.Path(a.dest)
    if dest.exists():
        for child in dest.iterdir():
            if child.name == ".git": continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    dest.mkdir(parents=True, exist_ok=True)
    manifest = []
    for s, d in items:
        out = dest / pathlib.Path(*d.parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        data = s.read_bytes()
        if s.suffix.lower() in TEXT_EXT or s.name in {".gitignore", ".gitattributes"}:
            data = data.replace(b"\r\n", b"\n")       # LF in the repo; .gitattributes keeps *.cmd/*.ps1 CRLF-safe on checkout
        out.write_bytes(data)
        manifest.append({"path": d.as_posix(), "sha256": hashlib.sha256(data).hexdigest()[:16], "bytes": len(data)})
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / "export-manifest.json").write_text(json.dumps({"files": len(manifest), "entries": manifest}, indent=1), encoding="utf-8")   # audit trail stays local
    print(f"exported {len(manifest)} files to {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
