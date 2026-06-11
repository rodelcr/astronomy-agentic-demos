# Checkpoint tags — aperture photometry

```bash
git checkout 03-photometry-step-3      # right after photometry passed
git diff   03-photometry-step-3 -- 03_photometry/project/scripts/photometry.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `03-photometry-step-1` | two failing tests (relative recovery + photutils) against a stub |
| `03-photometry-step-2` | seeded synthetic star field + `params.json` fluxes |
| `03-photometry-step-3` | `scripts/photometry.py` implemented; **both tests green** + CLI |
| `03-photometry-step-4` | `notebook.ipynb` (view → detect → measure → cross-check) |
| `03-photometry-step-5` | `make_figures.py` + `results/` aperture overlay & 1:1 compare |
| `03-photometry-step-6` | run on real M67 cutout; exact photutils agreement |
| `03-photometry-step-7` | `notes/` NOTES + HANDOFF |

> The `<=` vs `<` pixel-edge bug fixed inside step 3 is described in `TRANSCRIPT.md`.
