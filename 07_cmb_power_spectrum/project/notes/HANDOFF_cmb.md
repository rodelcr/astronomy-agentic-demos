# HANDOFF — CMB demo (capstone)

**TL;DR.** Fit a ΛCDM model (theory from CAMB) to the real Planck 2018 TT+TE power spectra
and recovered cosmological parameters:

> **H₀ = 67.0 km/s/Mpc, ωc = 0.121, Aₛ = 2.10** (Planck: 67.36 / 0.1200 / 2.100),
> **χ²/dof = 1.09**. The CMB's early-Universe H₀ = 67 vs demo 05's local 74.8 is the
> **Hubble tension**. Caveat: simplified Gaussian likelihood on binned spectra — not the
> official Planck analysis (see NOTES).

## What's here

| File | What it is |
|------|-----------|
| `scripts/cmb.py` | `theory_spectrum` (CAMB), `chi2`, `fit_cosmology`, `load_planck` + CLI |
| `scripts/make_figures.py` | fits real data; writes `results/tt_fit.png`, `te_fit.png`, `best_fit.json` |
| `tests/test_cmb.py` | injected-cosmology recovery + D_ℓ normalization vs CAMB |
| `data/real/planck_{tt,te}_binned.csv` | real Planck 2018 binned spectra (ESA PLA) |
| `data/synthetic/` | mock TT+TE from known cosmology + `params.json` |
| `notebook.ipynb` | peaks → units trap → fit → TT+TE → Hubble tension |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest                 # ~20 s
python scripts/make_figures.py
python scripts/cmb.py --tt data/real/planck_tt_binned.csv --te data/real/planck_te_binned.csv
```

## Validation status

- ✅ Recovers injected synthetic cosmology (H₀, ωc, Aₛ).
- ✅ D_ℓ normalization matches CAMB's hand-converted raw C_ℓ (1e-4).
- ✅ Real best-fit matches Planck 2018; χ²/dof ≈ 1.1; same parameters fit TT *and* TE.

## Outstanding / extensions

- Replace the point fit with a proper MCMC (emcee/cobaya) to get real posteriors and
  degeneracy contours (e.g. the H₀–ωc banana).
- Free up ωb and nₛ; add EE; add a τ prior.
- Use the actual bandpower window functions instead of effective-ℓ interpolation.
- Quantify the Hubble tension: compare this H₀ posterior to demo 05's bootstrap.
