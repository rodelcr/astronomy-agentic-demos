# HANDOFF — photometry demo

**TL;DR.** Implemented aperture photometry from scratch and measured star brightnesses
in a real M67 CCD image:

> Our hand-rolled aperture sums reproduce **`photutils` exactly** (max fractional
> difference 0), and recover known relative magnitudes to **0.02 mag** on synthetic
> stars. Brightest M67 stars: instrumental mag ≈ 11.

## What's here

| File | What it is |
|------|-----------|
| `scripts/photometry.py` | `aperture_flux`, `aperture_flux_raw`, `instrumental_mag`, `measure` + CLI |
| `scripts/make_figures.py` | regenerates `results/apertures.png`, `results/compare.png` |
| `tests/test_photometry.py` | relative-photometry recovery + exact photutils agreement |
| `data/real/m67_cutout.fits` | real Palomar Schmidt M67 cutout |
| `data/synthetic/` | seeded Gaussian-PSF field + `params.json` fluxes |
| `notebook.ipynb` | the exploratory narrative |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest
python scripts/make_figures.py
python scripts/photometry.py --image data/real/m67_cutout.fits --nbright 10
```

## Validation status

- ✅ Recovers injected relative magnitudes (0.02 mag).
- ✅ Matches photutils aperture sums exactly (rel 1e-6 → 0 in practice).

## Outstanding / extensions

- Fractional-pixel ("exact") apertures and compare to `method='exact'`.
- Aperture-correction / curve-of-growth to recover *total* (not just aperture) flux.
- A real zero point from standard stars to get calibrated magnitudes, then a CMD
  (hands off nicely to demo `04_gaia_cmd`).
