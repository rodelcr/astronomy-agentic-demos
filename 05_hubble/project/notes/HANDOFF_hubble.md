# HANDOFF — Hubble demo

**TL;DR.** Measured the Hubble constant from a real Cosmicflows-3 galaxy sample with a
through-origin fit and a bootstrap error bar:

> **H₀ = 74.8 ± 0.8 km/s/Mpc** (statistical) — local-ladder-consistent, above Planck's
> 67.4 (the Hubble tension). Caveat: bootstrap captures statistics, not the dominant
> distance-scale systematics.

## What's here

| File | What it is |
|------|-----------|
| `scripts/hubble.py` | `fit_h0` (through-origin), `bootstrap_h0` + CLI |
| `scripts/make_figures.py` | regenerates `results/hubble_diagram.png`, `results/bootstrap.png` |
| `tests/test_hubble.py` | injected-H₀ recovery + interval brackets truth + scipy match |
| `data/real/cosmicflows3.csv` | cached real Cosmicflows-3 distances & velocities |
| `data/synthetic/` | seeded Hubble flow at known H₀ + `params.json` |
| `notebook.ipynb` | diagram → fit → scipy check → bootstrap |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest
python scripts/make_figures.py
python scripts/hubble.py --data data/real/cosmicflows3.csv
```

## Validation status

- ✅ Recovers injected synthetic H₀ (5%); bootstrap interval brackets truth.
- ✅ Closed-form slope matches scipy curve_fit (1e-6).
- ✅ Real H₀ consistent with local distance-ladder measurements.

## Outstanding / extensions

- Weight the fit by per-galaxy distance errors (Cosmicflows provides them).
- Show the bias from including peculiar-velocity-dominated nearby galaxies (vary the cut).
- Compare bootstrap to a jackknife and to the analytic slope error.
