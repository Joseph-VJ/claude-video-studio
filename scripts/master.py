"""Compatibility CLI for the current quality-first exporter; no legacy extra encode."""
from pathlib import Path
import subprocess,sys
if __name__=="__main__":
    print("master.py delegates to export-instagram.py; use the current render workflow.",file=sys.stderr)
    raise SystemExit(subprocess.call([sys.executable,str(Path(__file__).with_name("export-instagram.py")),*sys.argv[1:]]))
