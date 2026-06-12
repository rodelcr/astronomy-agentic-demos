# CMB power spectrum — fitting cosmology to Planck (capstone)

## The problem

The cosmic microwave background is a snapshot of the Universe at 380,000 years old. Its
faint temperature ripples, summarized as a **power spectrum** — variance as a function of
angular scale (multipole ℓ) — carry a fingerprint of the cosmos: how much matter, how much
dark matter, how fast it expands. We fit a **ΛCDM** model to the real **Planck 2018** TT
(temperature) and TE (temperature–polarization) spectra and read off cosmological
parameters.

This is the **capstone**: the model isn't a closed form, it's a Boltzmann code (**CAMB**).
The skill is *inference* — likelihood, fit, validation — and *intellectual honesty* about
what's simplified.

## Physics scaffold

Before recombination, photons and baryons oscillate as sound waves; those frozen
oscillations appear as **acoustic peaks** in the power spectrum. The peak spacing measures
the geometry/expansion (→ H₀), the peak *heights* measure the matter densities (ωb, ωc),
and the overall amplitude/tilt measure the primordial fluctuations (Aₛ, nₛ).

The plotted quantity is

> **D_ℓ = ℓ(ℓ+1) C_ℓ / 2π   in μK²**

(not the raw C_ℓ — getting that factor or the μK scale wrong is the classic first CMB bug).
We compute D_ℓ with CAMB for trial parameters, compare to Planck via a χ², and minimize.

> Headline result: **H₀ = 67.0 km/s/Mpc, ωc = 0.121, Aₛ = 2.10** (Planck 2018: 67.36 /
> 0.1200 / 2.100), with **χ²/dof ≈ 1.1**. The CMB's *early-Universe* H₀ = 67 sits ~5σ below
> the *local* H₀ = 74.8 from demo `05_hubble` — the **Hubble tension**.

## What's in here

```
project/
  notebook.ipynb        peaks → units trap → CAMB theory → fit → TT+TE → Hubble tension
  scripts/cmb.py        theory_spectrum (CAMB), chi2, fit_cosmology — importable + CLI
  tests/test_cmb.py     recover injected cosmology + D_ℓ normalization matches CAMB
  data/
    real/planck_{tt,te}_binned.csv   real Planck 2018 binned spectra (ESA PLA)
    synthetic/                        make_synthetic.py + params.json (known cosmology)
  results/              tt_fit.png, te_fit.png, best_fit.json
  notes/                NOTES (simplifications + data source) + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest                 # ~20 s — runs CAMB many times (the slowest demo, by design)
python scripts/cmb.py --tt data/real/planck_tt_binned.csv --te data/real/planck_te_binned.csv
python scripts/make_figures.py
```

## External answer key

The model itself is **CAMB** (the standard Boltzmann code). We additionally validate our
**D_ℓ normalization** against CAMB's raw C_ℓ converted by hand — see
`tests/test_cmb.py::test_normalization_matches_camb` — and recover an injected cosmology
from mock data.

## Honesty — what's simplified (read this)

This is a teaching fit, **not** an official Planck analysis. We use a Gaussian likelihood
on the *public binned* spectra with diagonal errors (not the full `plik` likelihood,
covariance, or foreground/nuisance parameters); we sample theory at each bin's effective ℓ
(no bandpower windows); and we fit {H₀, ωc, Aₛ} with {ωb, nₛ, τ} fixed at the Planck
fiducial. A full 6-parameter analysis needs MCMC (cobaya/CosmoMC). Our values land close
to Planck, but the error bars are illustrative. Details in `notes/NOTES_cmb.md`.

## Data provenance

`data/real/planck_{tt,te}_binned.csv` are the **real** Planck 2018 binned CMB power spectra
(`COM_PowerSpect_CMB-TT-binned_R3.01`, `-TE-binned_R3.02`), downloaded from the ESA Planck
Legacy Archive. Columns: ℓ, D_ℓ (μK²), error, and Planck's own best-fit. Nothing fabricated.
