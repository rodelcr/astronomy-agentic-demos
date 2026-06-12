# HANDOFF — CMB map → power spectrum demo (capstone)

**TL;DR.** Computed the CMB angular power spectrum from a sky **map** by spherical-harmonic
decomposition (map → a_ℓm → Ĉ_ℓ = 1/(2ℓ+1)Σ_m|a_ℓm|² → bin), validated it against `healpy`
and **NaMaster**, fit ΛCDM to the result, and ran the same pipeline on the real Planck map.

> Injected H₀ = 69.0 → **recovered 69.19** (ωc, Aₛ on the nose) from a spectrum decomposed off an
> Nside-2048 map. `cl_from_alm` matches `healpy.alm2cl` to 7×10⁻¹⁵. First acoustic peak recovered
> from the **real** Planck SMICA map. The CMB's early-Universe H₀ ≈ 69 vs demo 05's local 74.8 =
> the Hubble tension.

This demo replaced an earlier binned-spectra version after a user correction; the rebuild's
intermediate problems (download truncation, API drift, pixel-window bias, binning artifact) are
cataloged in `notes/NOTES_cmb.md` and narrated in `walkthrough/TRANSCRIPT.md`.

## What's here

| File | What it is |
|------|-----------|
| `scripts/powerspectrum.py` | the SHT pipeline: `map_to_alm`, `cl_from_alm`, `pseudo_cl`, `bin_spectrum`, `namaster_bandpowers` + CLI |
| `scripts/cosmofit.py` | CAMB theory + `fit_cosmology` to map-derived bandpowers |
| `scripts/fetch_real_map.py` | rebuild the committed Nside-256 SMICA files from the archive |
| `scripts/make_figures.py` | regenerate the four figures + `best_fit.json` |
| `tests/test_powerspectrum.py`, `tests/test_cosmofit.py` | the four tests |
| `data/synthetic/` | `make_synthetic.py` + bandpowers + params.json |
| `data/real/planck_smica_{I,mask}_nside256.fits` | downgraded real Planck SMICA |
| `notebook.ipynb` | the full narrative |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py   # decompose an Nside-2048 map -> bandpowers
pytest                                      # 4 tests, ~25 s
python scripts/make_figures.py
# optional: rebuild the real-map files (downloads ~2 GB)
python scripts/fetch_real_map.py
```

## Validation status

- ✅ `cl_from_alm` matches `healpy.alm2cl` (7×10⁻¹⁵).
- ✅ Decomposed spectrum recovers the input C_ℓ (binned, few %).
- ✅ Masked pipeline agrees with NaMaster MASTER (~10%).
- ✅ Map-derived bandpowers fit recovers the injected cosmology.

## Outstanding / extensions

- Hand-roll the spin-2 (E/B) transform for TE/EE instead of delegating to healpy.
- Full MASTER + beam + half-mission noise debiasing on the real Nside-2048 map.
- Replace the χ² point fit with MCMC for posteriors and the H₀–ωc degeneracy contour.
- Quantify the Hubble tension against demo 05's bootstrap H₀.
