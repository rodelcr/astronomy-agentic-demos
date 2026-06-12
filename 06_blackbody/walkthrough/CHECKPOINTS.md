# Checkpoint tags — blackbody fit

```bash
git checkout 06-blackbody-step-3      # right after the fit passed
git diff   06-blackbody-step-3 -- 06_blackbody/project/scripts/blackbody.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `06-blackbody-step-1` | two failing tests (T recovery + astropy match) against a stub |
| `06-blackbody-step-2` | seeded synthetic Planck spectrum at known T + `params.json` |
| `06-blackbody-step-3` | `scripts/blackbody.py` implemented; **both tests green** + CLI |
| `06-blackbody-step-4` | `notebook.ipynb` (spectrum → fit → astropy → residuals) |
| `06-blackbody-step-5` | `make_figures.py` + `results/` FIRAS fit & residuals |
| `06-blackbody-step-6` | real FIRAS CMB result + literature check |
| `06-blackbody-step-7` | `notes/` NOTES (with source) + HANDOFF |

> The CGS-vs-MJy units bug fixed inside step 3 is described in `TRANSCRIPT.md`.
