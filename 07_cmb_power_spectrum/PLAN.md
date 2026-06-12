# Plan — CMB power spectrum → cosmological parameters

> Design doc, written before code. The capstone demo. `walkthrough/PROMPTS.md` executes
> this; `project/` is the result.

## Context

The cosmic microwave background's temperature and polarization anisotropies, summarized
as **power spectra** (TT, TE), are the most information-rich dataset in cosmology — their
acoustic-peak structure pins down the contents and geometry of the Universe. The student
fits a ΛCDM model to the **real Planck 2018** TT and TE binned spectra and recovers
cosmological parameters, including the early-Universe Hubble constant. Unlike the earlier
demos, the *model* is a Boltzmann code (**CAMB**) — too complex to hand-roll — so the
lesson shifts to **inference**: build a likelihood, fit parameters, validate against the
published answer, and **be explicit about every simplification**.

## The science (what we're measuring)

- **Input data:** the real Planck 2018 binned TT (83 bins) and TE (66 bins) power spectra
  (D_ℓ, errors); plus mock TT+TE generated from a known cosmology for the recovery test.
- **Method:** theory D_ℓ from CAMB; joint TT+TE Gaussian χ²; `scipy` minimization over a
  reduced parameter set {H₀, ωc, Aₛ} with {ωb, nₛ, τ} fixed at the Planck fiducial.
- **Headline output:** H₀ ≈ 67 km/s/Mpc, ωc ≈ 0.121, Aₛ ≈ 2.10 — matching Planck 2018,
  with χ²/dof ≈ 1.1. **H₀ from the early Universe**, to contrast with demo 05's local 74.8
  (the Hubble tension).
- **External answer key:** **CAMB** is the model engine; we additionally validate our
  D_ℓ = ℓ(ℓ+1)C_ℓ/2π μK² **normalization** against CAMB's raw C_ℓ converted by hand.

## Approach (and the alternative we rejected)

- **Chosen:** CAMB for theory + a simple χ² + a 3-parameter `scipy` fit on the public
  binned spectra. Tractable (~20 s), runs offline, and recovers Planck values — enough to
  teach the inference loop honestly.
- **Rejected:** the full Planck `plik` likelihood with its covariance and ~20
  foreground/nuisance parameters, sampled by MCMC (cobaya/CosmoMC). Correct, but hours of
  compute and thousands of lines — it would bury the lesson. We *name* it as the real thing.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | mock TT+TE from known cosmology (CAMB) + Planck-scaled noise + `params.json` |
| `data/real/planck_{tt,te}_binned.csv` | real Planck 2018 binned spectra (ESA PLA) |
| `scripts/cmb.py` | `theory_spectrum` (CAMB), `bin_to_data`, `chi2`, `fit_cosmology`, `load_planck`; CLI |
| `tests/test_cmb.py` | recover injected cosmology; D_ℓ normalization matches CAMB |
| `notebook.ipynb` | peaks → units trap → CAMB theory → fit → TT+TE → Hubble tension |
| `results/` | `tt_fit.png`, `te_fit.png`, `best_fit.json` |
| `notes/` | NOTES (simplifications + data source) + HANDOFF |

## Verification

- `pytest` green: injected-cosmology recovery **and** normalization-vs-CAMB (~20 s; the
  slowest demo, by design — it runs a Boltzmann code many times).
- `python scripts/cmb.py --tt ... --te ...` prints H₀/ωc/Aₛ vs Planck.
- `results/tt_fit.png` shows ΛCDM through the acoustic peaks, residuals consistent with
  the error bars.

## Risks / honesty (state these aloud)

- **Simplified likelihood:** Gaussian, diagonal errors on *binned* spectra — not the full
  Planck covariance + nuisance model. So parameters are *close to* Planck, not identical,
  and the error bars are not the official ones.
- **No bandpower windows:** theory is sampled at each bin's effective ℓ by interpolation.
- **Reduced parameter set:** {ωb, nₛ, τ} fixed; a full 6-parameter fit needs MCMC.
- **CAMB accuracy/lmax** set for speed; production work uses higher accuracy settings.
