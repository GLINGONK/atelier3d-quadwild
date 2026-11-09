# ATELIER 3D — QuadWild module

Optional quad-remeshing module for ATELIER 3D, installed from inside the application
(Auto-Retopo > Générer > « QuadWild (module) » > Installer). It is **not** bundled with
ATELIER 3D.

It packages the official Windows binaries of
[QuadWild with Bi-MDF solver](https://github.com/cgg-bern/quadwild-bimdf)
(Pietroni et al. 2021; Heistermann et al. 2023), unmodified. ATELIER 3D runs them as
separate programs (files in / files out).

## License

GNU GPL v3 — see [LICENSE](LICENSE). Each release contains:

- `quadwild-module-win64.zip` — `bin/quadwild.exe`, `bin/quad_from_patches.exe`, configs, LICENSE, NOTICE
- `quadwild-bimdf-source.zip` — the complete corresponding source code (with submodules)
- `manifest.json` — package URL, SHA-256 and command lines used by ATELIER 3D

## Building a release

`make_package.py` assembles the three files from the upstream release binaries and source.
