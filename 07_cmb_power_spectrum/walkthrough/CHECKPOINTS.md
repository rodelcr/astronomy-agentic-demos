# Checkpoint tags — CMB power spectrum

```bash
git checkout 07-cmb-step-3      # right after theory + fit passed
git diff   07-cmb-step-3 -- 07_cmb_power_spectrum/project/scripts/cmb.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `07-cmb-step-1` | two failing tests (cosmology recovery + CAMB normalization) vs a stub |
| `07-cmb-step-2` | mock TT+TE from a known cosmology + `params.json` |
| `07-cmb-step-3` | `scripts/cmb.py` (CAMB theory + χ² + fit); **both tests green** + CLI |
| `07-cmb-step-4` | `notebook.ipynb` (units trap → fit) |
| `07-cmb-step-5` | `make_figures.py` + `results/` TT & TE fits + `best_fit.json` |
| `07-cmb-step-6` | real Planck result + Hubble-tension framing |
| `07-cmb-step-7` | `notes/` NOTES (with simplifications) + HANDOFF |

> The C_ℓ-vs-D_ℓ / μK units bug fixed inside step 3 is described in `TRANSCRIPT.md`.
