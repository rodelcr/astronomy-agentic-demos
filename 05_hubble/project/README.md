# Hubble's law — measuring the expansion of the Universe

## The problem

Edwin Hubble found that galaxies recede from us at a speed proportional to their
distance. That proportionality, **v = H₀ d**, is the signature of an expanding
Universe, and its slope H₀ — the Hubble constant — sets the expansion rate and the
age of the cosmos. Here we measure H₀ from a real catalog of galaxy distances and
velocities.

## Physics scaffold

A galaxy at distance d recedes at v = H₀ d. Since a galaxy at zero distance has no
cosmological velocity, we fit a straight line **through the origin**; the
least-squares slope is the closed form

> **H₀ = Σ(d·v) / Σ(d²)   [km/s/Mpc]**

Real galaxies scatter around the line because of their own **peculiar velocities**, so
the slope alone isn't enough — we attach a **bootstrap** error bar: resample the
galaxies many times, refit, and read the spread.

> Headline result: **H₀ = 74.8 ± 0.8 km/s/Mpc** (statistical), consistent with local
> distance-ladder measurements and higher than Planck's early-Universe 67.4 — the
> "Hubble tension".

## What's in here

```
project/
  notebook.ipynb        diagram → through-origin fit → scipy cross-check → bootstrap
  scripts/hubble.py     fit_h0, bootstrap_h0 — importable + CLI
  tests/test_hubble.py  recover injected H0 (interval brackets truth) + match scipy
  data/
    real/cosmicflows3.csv    cached real Cosmicflows-3 (dist_mpc, vel_kms)
    synthetic/               make_synthetic.py + params.json (known H0)
  results/              hubble_diagram.png, bootstrap.png
  notes/                NOTES (incl. data source) + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/hubble.py --data data/real/cosmicflows3.csv
```

## External answer key

The through-origin slope is validated against **`scipy.optimize.curve_fit`** — see
`tests/test_hubble.py::test_agrees_with_scipy`. The bootstrap interval is checked to
bracket a known injected H₀ on synthetic data.

## Data provenance

`data/real/cosmicflows3.csv` is a 600-galaxy subsample of the **real** Cosmicflows-3
catalog (Tully et al. 2016, AJ 152, 50), distances and CMB-frame velocities, fetched
from VizieR (`J/AJ/152/50`) and cached. Cuts (10–200 Mpc, Vcmb > 500 km/s) are in
`notes/`. Nothing is fabricated.
