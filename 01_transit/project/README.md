# Exoplanet transit fit — the radius of Kepler-8 b

## The problem

A transiting planet blocks a sliver of its star's light once per orbit. The depth
of that dip tells you how big the planet is relative to its star. Here we measure
the radius ratio **Rp/R★** of the hot Jupiter **Kepler-8 b** from a real quarter of
Kepler photometry.

## Physics scaffold

A star of radius R★ has projected area ∝ R★². A planet of radius Rp covering part
of the disk blocks an area ∝ Rp². If the star were uniformly bright, the fractional
drop in light during transit is exactly

> **δ = (Rp / R★)²   ⟹   Rp/R★ = √δ**

So measuring the transit *depth* δ measures the *size* of the planet. (Real stars
are limb-darkened — brighter at center — so the true dip is a little deeper than
δ; see `notes/`. We handle this honestly: the synthetic test and the `batman`
agreement test use a uniform source where the relation is exact.)

To measure δ we **phase-fold**: the planet transits every period P, so we wrap all
the data onto a single orbit (phase = fractional position in the orbit) and the
scattered transits stack into one clean dip, which we fit with a trapezoid.

> Headline result: **Rp/R★ ≈ 0.094** for Kepler-8 b (literature: 0.0944, Jenkins
> et al. 2010 — a Jupiter-sized planet).

## What's in here

```
project/
  notebook.ipynb        explore the real curve → fold → fit → inspect residuals
  scripts/transit.py    phase_fold, fit_transit, rp_over_rstar — importable + CLI
  tests/test_transit.py recover injected depth + agree with batman
  data/
    real/kepler8_q3.csv     real Kepler-8 quarter (time_bkjd, flux, flux_err)
    synthetic/              make_synthetic.py + params.json ground truth
  results/              folded_fit.png, residuals.png
  notes/                NOTES + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/transit.py --data data/real/kepler8_q3.csv --period 3.52254 --t0 120.0
```

## External answer key

The fit is validated against **`batman`** (Mandel & Agol 2002), the standard
transit-model code — see `tests/test_transit.py::test_agrees_with_batman`.

## Data provenance

`data/real/kepler8_q3.csv` is **real** Kepler long-cadence photometry of KIC
6922244 (Kepler-8), quarter starting BKJD 2009-259, downloaded from MAST and
median-normalized (PDCSAP flux). Nothing here is fabricated.
