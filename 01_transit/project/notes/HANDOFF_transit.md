# HANDOFF — transit demo

**TL;DR.** Measured the radius ratio of the hot Jupiter **Kepler-8 b** from one
quarter of real Kepler photometry by phase-folding and fitting a trapezoid:

> **Rp/R★ = 0.0935** (literature 0.0944, Jenkins et al. 2010) — a Jupiter-sized planet.

## What's here

| File | What it is |
|------|-----------|
| `scripts/transit.py` | `phase_fold`, `fit_transit`, `rp_over_rstar` — importable + CLI |
| `scripts/make_figures.py` | regenerates `results/folded_fit.png`, `results/residuals.png` |
| `tests/test_transit.py` | (a) recover injected synthetic depth; (b) agree with `batman` |
| `data/real/kepler8_q3.csv` | real Kepler-8 quarter (PDCSAP, median-normalized) |
| `data/synthetic/` | seeded generator + `params.json` ground truth |
| `notebook.ipynb` | the exploratory narrative |

## How to reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py    # regenerate synthetic data
pytest                                       # both tests green
python scripts/make_figures.py               # regenerate figures
python scripts/transit.py --data data/real/kepler8_q3.csv --period 3.52254 --t0 170.4408
```

## Validation status

- ✅ Recovers injected synthetic depth (5% tol).
- ✅ Agrees with `batman` uniform-source model (3% tol).
- ✅ Real-data Rp/R★ within 1% of literature.

## Outstanding / extensions

- Fit limb-darkening with the full `batman` model and compare Rp/R★ (expect the ~1%
  gap to close). Good "next iteration" for a student.
- Recover the period independently with `BoxLeastSquares` instead of assuming it.
- Propagate flux errors into an uncertainty on Rp/R★ (bootstrap the folded points).
