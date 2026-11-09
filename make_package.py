"""Build the ATELIER 3D QuadWild module release (build tool, never shipped with the app).

Inputs : tools/quadwild/dl/win   (official cgg-bern/quadwild-bimdf v0.0.2 Windows binaries)
         tools/quadwild/src      (matching GPL-3 source, with submodules)
Outputs: tools/quadwild/out/{quadwild-module-win64.zip, manifest.json, quadwild-bimdf-source.zip}
Run    : runtime\\python.exe tools\\quadwild\\make_package.py <version>
"""

import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else "0.0.2-1"
OWNER, REPO = "GLINGONK", "atelier3d-quadwild"
BASE = f"https://github.com/{OWNER}/{REPO}/releases/download/v{VERSION}/"

NOTICE = """QuadWild with Bi-MDF solver — packaged as an optional ATELIER 3D module.

Upstream : https://github.com/cgg-bern/quadwild-bimdf (fork of nicopietroni/quadwild)
Authors  : Nico Pietroni, Stefano Nuvoli, Thomas Alderighi, Paolo Cignoni, Marco Tarini
           (QuadWild); Martin Heistermann, Jethro Warnett, David Bommes (Bi-MDF).
License  : GNU GPL v3 (see LICENSE). The complete corresponding source code is published
           with every release of this repository (quadwild-bimdf-source.zip).
These programs are separate executables run by ATELIER 3D in their own process.
"""


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    win, src, out = HERE / "dl" / "win", HERE / "src", HERE / "out"
    out.mkdir(exist_ok=True)
    stage = out / "stage"
    shutil.rmtree(stage, ignore_errors=True)
    (stage / "bin").mkdir(parents=True)
    for exe in ("quadwild.exe", "quad_from_patches.exe"):
        shutil.copy2(win / exe, stage / "bin" / exe)
    for dll in win.glob("*.dll"):
        shutil.copy2(dll, stage / "bin" / dll.name)
    shutil.copytree(win / "config", stage / "config")
    (stage / "results").mkdir()                        # quad_from_patches writes debug here
    shutil.copy2(src / "LICENSE", stage / "LICENSE")
    (stage / "NOTICE.txt").write_text(NOTICE, encoding="utf-8")

    pkg = out / "quadwild-module-win64.zip"
    with zipfile.ZipFile(pkg, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(stage).as_posix())
    shutil.rmtree(stage)

    srczip = out / "quadwild-bimdf-source.zip"
    with zipfile.ZipFile(srczip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            rel = f.relative_to(src)
            if f.is_file() and ".git" not in rel.parts:
                z.write(f, ("quadwild-bimdf/" + rel.as_posix()))

    man = {
        "id": "quadwild", "name": "QuadWild (Bi-MDF)", "version": VERSION,
        "license": "GPL-3.0", "source_url": BASE + srczip.name,
        "package": {"url": BASE + pkg.name, "sha256": sha(pkg)},
        "flow_config": "config/main_config/flow_noalign_lemon.txt",
        "steps": [
            ["{exe:quadwild}", "{mesh}", "2", "{res:config/prep_config/basic_setup.txt}"],
            ["{exe:quad_from_patches}", "{stem}_rem_p0.obj", "0", "{flow}"],
        ],
        "outputs": {"mesh": "{stem}_rem_p0_0_quadrangulation_smooth.obj",
                    "fallback": ["{stem}_rem_p0_0_quadrangulation.obj"]},
    }
    (out / "manifest.json").write_text(json.dumps(man, indent=2), encoding="utf-8")
    for f in (pkg, srczip, out / "manifest.json"):
        print(f.name, f.stat().st_size)


if __name__ == "__main__":
    main()
