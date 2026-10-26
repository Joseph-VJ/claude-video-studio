"""Make a cloned studio run from any folder.

The studio was built at E:/Video and its instructions, scripts and settings name that folder. `apply` rewrites those references to the
folder you cloned into (and the bundled Chrome paths to your installed Chrome); `revert` restores the files from git so `git pull` is clean.

  python scripts/studio-portable.py apply  --root C:/VideoStudio [--chrome "C:/Program Files/Google/Chrome/Application/chrome.exe"]
  python scripts/studio-portable.py revert
  python scripts/studio-portable.py status

State lives in .studio-portable.json (git-ignored). Running `apply` again with the same arguments changes nothing.
"""
import argparse, json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent.parent
STATE = HERE / ".studio-portable.json"
ORIGIN = "E:/Video"
SKIP_DIRS = {".git", "node_modules", ".venv", "cache", "models", "out", "raw", "work", "logs", "repos", "tools", "__pycache__", ".agents", "projects_local"}
TEXT_EXT = {".md", ".py", ".ps1", ".cmd", ".json", ".txt", ".ts", ".tsx", ".js", ".cjs", ".mjs", ".html", ".css", ".yml", ".yaml", ".toml"}
CHROME_FORMS = [r"E:\Video\tools\chrome\chrome-win64\chrome.exe", r"E:\Video\tools\chrome-headless\chrome-headless-shell-win64\chrome-headless-shell.exe"]
ROOT_RX = re.compile(r"E:(?P<sep>\\\\|\\|/)Video(?![A-Za-z0-9_-])")


def git_files():
    try:
        out = subprocess.run(["git", "-C", str(HERE), "ls-files"], capture_output=True, text=True, check=True).stdout
        return [HERE / l for l in out.splitlines() if l]
    except Exception:
        return [p for p in HERE.rglob("*") if p.is_file() and not (set(p.relative_to(HERE).parts) & SKIP_DIRS)]


def candidates():
    for p in git_files():
        if p.suffix.lower() in TEXT_EXT and p.is_file() and p.name != "studio-portable.py" and not (set(p.relative_to(HERE).parts) & SKIP_DIRS):
            yield p


def forms(root: str):
    r = root.replace("/", "\\").rstrip("\\")
    return {"/": r.replace("\\", "/"), "\\": r, "\\\\": r.replace("\\", "\\\\")}


def rewrite(text: str, root: str, chrome: str | None):
    f = forms(root)
    if chrome:
        for old in CHROME_FORMS:
            for o, n in ((old, chrome), (old.replace("\\", "/"), chrome.replace("\\", "/")), (old.replace("\\", "\\\\"), chrome.replace("\\", "\\\\"))):
                text = text.replace(o, n)
    return ROOT_RX.sub(lambda m: f[m.group("sep")], text)


def cmd_apply(a):
    root = os.path.abspath(a.root).replace("\\", "/")
    # Safety: this tool only ever rewrites the folder it lives in, and only a git clone (so `revert` can always restore the files).
    if pathlib.Path(root).resolve() != HERE.resolve():
        sys.exit(f"refusing: this copy of the tool lives in {HERE} but --root is {root}. It only rewrites its own folder; run the copy inside the clone you want to change.")
    if not (HERE / ".git").exists():
        sys.exit(f"refusing: {HERE} is not a git clone, so the rewrite could not be undone.")
    chrome = a.chrome.replace("/", "\\") if a.chrome else None
    if root.lower() == ORIGIN.lower():
        print("root is already E:/Video: nothing to rewrite"); return 0
    if STATE.exists():
        old = json.loads(STATE.read_text(encoding="utf-8"))
        if old.get("root") != root or old.get("chrome") != chrome:
            print("Previous rewrite found for a different root/chrome: reverting it first")
            cmd_revert(a)
    changed = []
    for p in candidates():
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        n = rewrite(t, root, chrome)
        if n != t:
            p.write_text(n, encoding="utf-8", newline="")
            changed.append(p.relative_to(HERE).as_posix())
    prev = json.loads(STATE.read_text(encoding="utf-8")).get("files", []) if STATE.exists() else []
    STATE.write_text(json.dumps({"root": root, "chrome": chrome, "files": sorted(set(prev) | set(changed))}, indent=1), encoding="utf-8")
    print(f"rewrote {len(changed)} files to {root}" + (f" (Chrome: {chrome})" if chrome else ""))
    return 0


def cmd_revert(a):
    if not STATE.exists():
        print("nothing to revert"); return 0
    files = json.loads(STATE.read_text(encoding="utf-8")).get("files", [])
    if files:
        subprocess.run(["git", "-C", str(HERE), "checkout", "--", *files], check=True)
    STATE.unlink()
    print(f"restored {len(files)} files from git")
    return 0


def cmd_status(a):
    print(STATE.read_text(encoding="utf-8") if STATE.exists() else "no rewrite applied (files still reference E:/Video)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("apply"); s.add_argument("--root", required=True); s.add_argument("--chrome"); s.set_defaults(f=cmd_apply)
    sub.add_parser("revert").set_defaults(f=cmd_revert)
    sub.add_parser("status").set_defaults(f=cmd_status)
    a = ap.parse_args()
    sys.exit(a.f(a))
