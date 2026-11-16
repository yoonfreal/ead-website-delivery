"""Validate, stage and package the classroom site without external packages."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from check_site import validate_site

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"

def git_value(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT,
            stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "local-uncommitted"

def main():
    print(validate_site(SRC))
    # Remove only the generated directory under this starter project.
    if DIST.exists():
        shutil.rmtree(DIST)
    site = DIST / "site"
    shutil.copytree(SRC, site)
    info = {
        "commit": os.getenv("GITHUB_SHA") or git_value("rev-parse", "HEAD"),
        "branch": os.getenv("GITHUB_REF_NAME") or git_value("branch", "--show-current"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "source_files_sha256": {
            str(p.relative_to(SRC)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(SRC.rglob("*")) if p.is_file()
        }
    }
    (DIST / "build-info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    (site / "build-info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    with zipfile.ZipFile(DIST / "site.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
        for p in sorted(site.rglob("*")):
            if p.is_file():
                bundle.write(p, p.relative_to(site))
    print("Built dist/site.zip and dist/build-info.json")

if __name__ == "__main__":
    main()
