# CMB map → power spectrum → cosmology (capstone)

## The problem

A CMB experiment hands you a **map** of the microwave sky. The cosmology lives in its
**angular power spectrum** — and getting from the map to the spectrum is a real computation:
the **spherical-harmonic decomposition**. This demo does it explicitly, on a synthetic
Nside-2048 sky and on the real Planck map, then fits a cosmological model to the result.

> This demo was **rebuilt after a correction**: the first version fit Planck's pre-binned
> spectra and skipped the decomposition. The user asked for the real thing — from the Nside-2048
> maps. The story is in `walkthrough/TRANSCRIPT.md`, which catalogs the intermediate problems
> that rebuild surfaced (a flaky 2 GB download, an API quirk, two numerical biases) and how
> agentic coding solved each.

## Physics scaffold

Any temperature field on the sphere expands in spherical harmonics:

> **T(n̂) = Σ_ℓm a_ℓm Y_ℓm(n̂)**,  with  **a_ℓm = ∫ T(n̂) Y*_ℓm(n̂) dΩ**

`healpy.map2alm` evaluates that integral. The **angular power spectrum** is the variance of
the coefficients at each scale ℓ:

> **Ĉ_ℓ = 1/(2ℓ+1) Σ_{m=-ℓ}^{ℓ} |a_ℓm|²**

`cl_from_alm` computes that m-sum by hand (HEALPix stores only m ≥ 0, so for a real map it's
|a_{ℓ0}|² + 2Σ_{m≥1}|a_ℓm|²) and is checked against `healpy.alm2cl`. Finite pixels smooth the
map (the pixel window w_ℓ) — divide it out. Real skies are masked (the Galaxy is cut), which
couples multipoles; the rigorous deconvolution is **NaMaster** (MASTER).

> Headline result: from a spectrum we **decomposed out of an Nside-2048 map**, we recover the
> injected cosmology (**H₀ ≈ 69**, ωc, Aₛ on the nose); the masked pipeline matches NaMaster; and
> the first acoustic peak emerges from the **real** Planck SMICA map.

## What's in here

```
project/
  notebook.ipynb            sky → SHT → spectrum → masking/NaMaster → fit → real sky
  scripts/powerspectrum.py  map_to_alm, cl_from_alm, pseudo_cl, bin_spectrum, namaster_bandpowers — + CLI
  scripts/cosmofit.py       CAMB theory + fit_cosmology to map-derived bandpowers
  scripts/fetch_real_map.py download the real SMICA map and make the committed Nside-256 files
  tests/test_powerspectrum.py  cl_from_alm vs healpy + recover input spectrum + NaMaster agreement
  tests/test_cosmofit.py    recover injected cosmology from the bandpowers
  data/
    real/planck_smica_{I,mask}_nside256.fits   downgraded REAL Planck SMICA (committed)
    synthetic/              make_synthetic.py + bandpowers_{tt,te}.csv + params.json
  results/                  map_and_spectrum.png, masking_namaster.png, cosmology_fit.png, real_smica.png
  notes/                    NOTES (incl. intermediate-problems catalog) + HANDOFF
  requirements.txt
```

The Nside-2048 map (~400 MB) is **not** committed — it is regenerated deterministically from a
seed. The committed data product is the small **bandpowers** CSV (the spectrum measured off the
map), the params, and the downgraded real map.

## Run it

```bash
conda activate demos
pytest                              # ~25 s — runs CAMB, an Nside-1024 SHT, and NaMaster
python data/synthetic/make_synthetic.py      # decompose an Nside-2048 map into bandpowers
python scripts/powerspectrum.py --nside 2048 --lmax 2000
python scripts/make_figures.py
```

## External answer keys

`healpy.alm2cl` validates the hand-rolled `cl_from_alm`; **NaMaster** validates the masked
pipeline (`tests/test_powerspectrum.py`). The cosmology fit is checked by recovering an injected
cosmology from the map-derived bandpowers.

## Data provenance

The synthetic sky is a Gaussian realization (synfast) of a CAMB spectrum — generated, not
fabricated, regenerable from the seed in `params.json`. The real map
(`data/real/planck_smica_*_nside256.fits`) is the **real** Planck SMICA CMB map (Fixsen/Planck
2018), temperature + confidence mask, downgraded from Nside 2048 to 256; reproduce it with
`scripts/fetch_real_map.py`. Nothing is fabricated.
