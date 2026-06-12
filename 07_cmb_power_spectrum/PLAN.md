# Plan — CMB map → power spectrum → cosmology

> Design doc, written before code. The capstone. `walkthrough/PROMPTS.md` executes this.
>
> **Revised after a course-correction:** the first version fit Planck's pre-binned spectra.
> The user asked for the real computation — from **Nside 2048 maps**, showing the
> **spherical-harmonic decomposition**. This plan reflects that rebuild; the back-and-forth
> is documented in `walkthrough/TRANSCRIPT.md`.

## Context

A CMB experiment delivers a **map** of the microwave sky; the cosmology lives in its
**angular power spectrum**. Getting from one to the other is the spherical-harmonic
transform: expand the map in spherical harmonics Y_ℓm to get coefficients a_ℓm, then form
Ĉ_ℓ = 1/(2ℓ+1) Σ_m |a_ℓm|². This demo does that explicitly on a synthetic Nside-2048 sky
(offline), validates it against `healpy` and **NaMaster**, fits ΛCDM to the map-derived
bandpowers, and finally runs the same pipeline on the real Planck SMICA map.

## The science (what we're computing)

- **Input:** a synthetic Nside-2048 Gaussian CMB map drawn (synfast) from a CAMB theory C_ℓ
  with a known cosmology; plus a downgraded (Nside 256) real Planck SMICA map for a check.
- **Method:** map → a_ℓm (`healpy.map2alm`) → Ĉ_ℓ = 1/(2ℓ+1)Σ_m|a_ℓm|² (hand-rolled in
  `cl_from_alm`) → pixel-window correction → bin. Masked sky: fsky correction (naive) vs
  NaMaster MASTER (rigorous). Then fit {H₀, ωc, Aₛ} to the TT bandpowers with cosmic-variance
  errors. TE comes from the spin-2 (polarization) transform via healpy.
- **Headline:** recover the injected cosmology (H₀ ≈ 69) from a spectrum we built out of a
  map; reproduce the first acoustic peak from the real Planck sky.
- **External answer keys:** `healpy.alm2cl` (validates our by-hand estimator) and **NaMaster**
  (validates the masked pipeline).

## Approach (and the alternatives rejected)

- **Chosen:** hand-rolled `cl_from_alm` (so the decomposition is visible), healpy for the SHT
  integral and spin-2 transforms, NaMaster for masked mode-coupling. Synthetic Nside-2048 map
  regenerated from seed (not shipped); the committed data is the small bandpowers CSV.
- **Rejected — pre-binned spectra:** the original shortcut; it hides the entire computation.
- **Rejected — full MASTER + half-mission noise debiasing by hand:** we *use* NaMaster for the
  rigorous masked estimator rather than reimplementing it.

## Components

| File | Responsibility |
|------|----------------|
| `scripts/powerspectrum.py` | `generate_cmb_map`, `map_to_alm`, `cl_from_alm`, `pseudo_cl`, `bin_spectrum`, `namaster_bandpowers`; CLI |
| `scripts/cosmofit.py` | CAMB `theory_spectrum`/`theory_cl_tt`, `cosmic_variance`, `fit_cosmology` |
| `scripts/fetch_real_map.py` | download the real SMICA map + downgrade to the committed Nside-256 files |
| `data/synthetic/make_synthetic.py` | build the Nside-2048 map, decompose it, write bandpowers + params.json |
| `data/real/planck_smica_{I,mask}_nside256.fits` | downgraded real Planck SMICA (committed, ~3 MB each) |
| `tests/test_powerspectrum.py` | cl_from_alm vs healpy; recover input spectrum; NaMaster agreement |
| `tests/test_cosmofit.py` | recover injected cosmology from the map-derived bandpowers |
| `notebook.ipynb` | sky → SHT → spectrum → masking/NaMaster → fit → real sky |
| `results/` | map_and_spectrum, masking_namaster, cosmology_fit, real_smica, best_fit.json |

## Verification

- `pytest` green: 3 pipeline tests + 1 cosmology-recovery test (~25 s; slowest demo, runs CAMB
  + Nside-1024 SHT + NaMaster).
- `python scripts/powerspectrum.py --nside 2048 --lmax 2000` decomposes a map and prints the
  recovery ratio.
- `results/map_and_spectrum.png` shows the sky and the spectrum we pulled out of it.

## Risks / honesty

- The synthetic map carries the **pixel window** so the pixwin² correction is exact (a bias
  here cost 2% — see TRANSCRIPT). Compare binned-to-binned, never binned-to-bin-centre.
- The real-data check is **downgraded (Nside 256, ℓ ≲ 500)** and uses the naive fsky estimator —
  a sanity check, not a Planck-grade analysis. Beam, noise debiasing, and full MASTER on the
  real map are extensions.
- TE uses the spin-2 transform (delegated to healpy); the hand-rolled estimator is shown for the
  scalar TT case.
