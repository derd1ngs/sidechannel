"""Build the static browser version into OUT_DIR (default: _site/).

Copies the page assets from web/ and zips just the Python the page runs in
Pyodide -- sidechannel/__init__.py, engine/, stories/ and web_bridge.py,
never the Textual frontend. The zip's content hash is stamped into app.js
and the service worker (sw.js), so a new deploy is never served a stale
cached zip and replaces the offline cache.

The Pyodide runtime is served from the site too (D17): the pinned release's
core files, checked against PYODIDE_CORE_SHA256, plus the packages the game
loads, checked against the hashes in that release's pyodide-lock.json.
Downloads are kept in .cache/pyodide/ for the next build.

    python web/build.py [OUT_DIR]
    python -m http.server -d _site 8000    # then open http://localhost:8000
"""

from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT / "web"
PACKAGE_DIR = ROOT / "sidechannel"
ASSETS = ["index.html", "style.css", "favicon.svg", "favicon-32.png", "apple-touch-icon.png"]
STAMPED = ["app.js", "sw.js"]  # get the build id in place of __BUILD_ID__
PYTHON_PARTS = ["__init__.py", "engine", "stories", "web_bridge.py"]

# A new Pyodide: bump PYODIDE_VERSION and PYODIDE_CORE_SHA256, and PYODIDE_DIR in app.js and sw.js.
PYODIDE_VERSION = "314.0.7"
PYODIDE_CORE_URL = f"https://github.com/pyodide/pyodide/releases/download/{PYODIDE_VERSION}/pyodide-core-{PYODIDE_VERSION}.tar.bz2"
PYODIDE_CORE_SHA256 = "2abdcc2e35208af406e07724cffa85bc582ced97e9028383ecf5462541393f95"
PYODIDE_PACKAGES_URL = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/"
PYODIDE_DIR = f"pyodide-{PYODIDE_VERSION}"  # versioned, so no cache ever mixes two releases
PYODIDE_FILES = [
    "pyodide.mjs",
    "pyodide.asm.mjs",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]
PYODIDE_PACKAGES = ["pyyaml"]  # what app.js passes to loadPackage
CACHE_DIR = ROOT / ".cache" / "pyodide"


class DownloadError(Exception):
    pass


def fetch_verified(url: str, sha256: str) -> bytes:
    """`url`'s content, from the cache or downloaded; refused unless its
    sha256 matches."""
    cached = CACHE_DIR / sha256
    data = cached.read_bytes() if cached.exists() else urllib.request.urlopen(url, timeout=120).read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != sha256:
        raise DownloadError(f"{url}: sha256 {actual}, expected {sha256}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data


def copy_pyodide(out_dir: Path) -> None:
    dest = out_dir / PYODIDE_DIR
    dest.mkdir(parents=True, exist_ok=True)
    core = fetch_verified(PYODIDE_CORE_URL, PYODIDE_CORE_SHA256)
    with tarfile.open(fileobj=io.BytesIO(core), mode="r:bz2") as tar:
        for name in PYODIDE_FILES:
            member = tar.extractfile(f"pyodide/{name}")
            assert member is not None
            (dest / name).write_bytes(member.read())
    lock = json.loads((dest / "pyodide-lock.json").read_text())
    for package in PYODIDE_PACKAGES:
        entry = lock["packages"][package]
        assert not entry["depends"], f"{package}'s dependencies need adding to PYODIDE_PACKAGES"
        wheel = fetch_verified(PYODIDE_PACKAGES_URL + entry["file_name"], entry["sha256"])
        (dest / entry["file_name"]).write_bytes(wheel)


def python_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for part in PYTHON_PARTS:
            src = PACKAGE_DIR / part
            files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
            for path in files:
                if "__pycache__" in path.parts:
                    continue
                # Fixed timestamp: the same sources always give the same zip (and hash).
                info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2000, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def compute_build_id(data: bytes) -> str:
    """A hash of everything the site ships -- the Python zip *and* every web
    file. The service worker is only replaced when sw.js changes, and this id
    is stamped into it, so a change to any shipped file must change the id
    (or offline players would keep the old page forever)."""
    digest = hashlib.sha256(data)
    for name in ASSETS + STAMPED:
        digest.update((WEB_DIR / name).read_bytes())
    return digest.hexdigest()[:12]


def build(out_dir: Path, with_pyodide: bool = True) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    if with_pyodide:
        copy_pyodide(out_dir)
    for name in ASSETS:
        shutil.copyfile(WEB_DIR / name, out_dir / name)
    data = python_zip()
    (out_dir / "sidechannel.zip").write_bytes(data)
    build_id = compute_build_id(data)
    for name in STAMPED:
        (out_dir / name).write_text((WEB_DIR / name).read_text().replace("__BUILD_ID__", build_id))
    print(f"Built {out_dir} (build {build_id})")


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site")
