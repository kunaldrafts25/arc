"""Run the official CLI using the gitignored project-local Kaggle token."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
token_file = ROOT / ".kaggle/access_token"
if not token_file.is_file():
    raise SystemExit("Save the Kaggle token in .kaggle/access_token first")
token = token_file.read_text(encoding="utf-8-sig").strip()
if not token:
    raise SystemExit("The project-local Kaggle token file is empty")
environment = os.environ.copy()
environment["KAGGLE_API_TOKEN"] = token
environment["KAGGLE_CONFIG_DIR"] = str(token_file.parent)
environment["PYTHONUTF8"] = "1"
raise SystemExit(subprocess.call([sys.executable, "-m", "kaggle", *sys.argv[1:]],
                                cwd=ROOT, env=environment))
