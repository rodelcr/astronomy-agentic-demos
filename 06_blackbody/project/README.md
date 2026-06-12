# Blackbody fit — the temperature of the Universe

## The problem

A perfect absorber re-emits a spectrum — the **blackbody** or Planck spectrum — whose
shape and brightness are fixed entirely by its **temperature**. Fit that curve to a
measured spectrum and you read off the temperature. Here we do it for the **cosmic
microwave background** using the famous COBE/FIRAS data — the most perfect blackbody
ever measured.

## Physics scaffold

The Planck law gives the spectral radiance of a blackbody at temperature T:

> **B_ν(T) = (2hν³ / c²) · 1 / (exp(hν/kT) − 1)**

It depends on a *single* parameter, T. Because the FIRAS spectrum is absolutely
calibrated (real MJy/sr, not arbitrary units), we fit the absolute Planck curve with no
free scale, and T is the only thing to solve for.

> Headline result: **T = 2.725 K** (literature 2.72548 ± 0.00057 K, Fixsen 2009) — the
> temperature of the Universe.

## What's in here

```
project/
  notebook.ipynb        spectrum → Planck fit → astropy cross-check → residuals
  scripts/blackbody.py  planck_MJy, fit_temperature — importable + CLI
  tests/test_blackbody.py  recover injected T + Planck matches astropy
  data/
    real/firas_cmb.csv       real COBE/FIRAS CMB monopole spectrum
    synthetic/               make_synthetic.py + params.json (known T)
  results/              firas_fit.png, residuals.png
  notes/                NOTES (incl. data source) + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/blackbody.py --data data/real/firas_cmb.csv
```

## External answer key

Our Planck function is validated against **`astropy.modeling.BlackBody`** in absolute
units — see `tests/test_blackbody.py::test_planck_matches_astropy`.

## Data provenance

`data/real/firas_cmb.csv` is the **real** COBE/FIRAS CMB monopole spectrum (Fixsen et
al. 1996, ApJ 473, 576), downloaded from NASA LAMBDA: frequency (cm⁻¹), monopole
intensity (MJy/sr), 1σ uncertainty. Nothing is fabricated.
