# HANDOFF — blackbody demo

**TL;DR.** Fit the Planck law to the real COBE/FIRAS CMB spectrum and recovered the
temperature of the Universe:

> **T = 2.725 K** (literature 2.72548 ± 0.00057 K). Our Planck function matches
> `astropy.modeling.BlackBody` to 1e-4; residuals flat to < 0.01% (a near-perfect blackbody).

## What's here

| File | What it is |
|------|-----------|
| `scripts/blackbody.py` | `planck_MJy`, `fit_temperature` + CLI |
| `scripts/make_figures.py` | regenerates `results/firas_fit.png`, `results/residuals.png` |
| `tests/test_blackbody.py` | injected-T recovery + Planck-vs-astropy match |
| `data/real/firas_cmb.csv` | real COBE/FIRAS CMB monopole spectrum |
| `data/synthetic/` | seeded Planck spectrum at known T + `params.json` |
| `notebook.ipynb` | spectrum → fit → astropy check → residuals |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest
python scripts/make_figures.py
python scripts/blackbody.py --data data/real/firas_cmb.csv
```

## Validation status

- ✅ Recovers injected synthetic T (1% tol).
- ✅ Planck function matches astropy.modeling.BlackBody (1e-4, absolute units).
- ✅ Real T within the FIRAS literature value.

## Outstanding / extensions

- Fit a real *stellar* SED (broadband photometry) where a single blackbody is only
  approximate — a good contrast to the CMB's perfection.
- Add a Wien-displacement sanity check (peak frequency ↔ T).
- Propagate the FIRAS uncertainties into a formal T error bar and compare to Fixsen 2009.
