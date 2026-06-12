# Prompt walkthrough — CMB power spectrum (capstone)

The agentic-coding side. Paste each step into Claude Code in your own empty folder, one at
a time; read the diff and look at the output before continuing. This is the most ambitious
demo — the model is a Boltzmann code (CAMB), so the emphasis is inference and **honesty
about simplifications**. Compare against `../project/` and `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 07_cmb_power_spectrum/PLAN.md and project/README.md. What are we measuring, what
computes the theory, and what do we validate? List every simplification the README admits
to. No code yet.
```
**Look for:** "theory from CAMB; validate our D_ℓ normalization + recover injected cosmology;
simplified Gaussian likelihood on binned spectra, reduced parameters." If it can't list the
caveats, it doesn't understand the demo.

### Step 1 — Tests first (red)
```
Write tests/test_cmb.py + a stub scripts/cmb.py so they import and fail:
  1. test_recovers_injected_cosmology — fit mock TT+TE of known (H0, ωc, As), recover them.
  2. test_normalization_matches_camb — assert our theory D_ℓ equals CAMB's raw C_ℓ converted
     by hand with ℓ(ℓ+1)/2π and the μK² factor.
Run pytest, show red. Commit "step 1: failing tests".
```
**Look for:** the normalization test is the student-owned check (we can't re-derive CAMB's
physics, but we *can* check our unit handling).

### Step 2 — Mock data from a known cosmology
```
Write data/synthetic/make_synthetic.py: compute TT+TE with CAMB at chosen parameters
(offset from the Planck fiducial), sample at the real Planck bins' multipoles, add Gaussian
noise scaled to the real error bars. Save mock_tt.csv, mock_te.csv, params.json. Run it.
Commit "step 2: mock data + truth".
```
**Look for:** the noise model reuses the *real* Planck error bars — realistic, not arbitrary.

### Step 3 — Implement theory + likelihood + fit (green)
```
Implement scripts/cmb.py: theory_spectrum(H0, ωc, As, ...) wrapping CAMB and returning D_ℓ
in μK² for TT and TE; bin_to_data (interpolate to data multipoles); chi2 (joint TT+TE);
fit_cosmology via scipy minimize over {H0, ωc, As}. Make both tests pass; add a CLI.
Commit "step 3: theory + fit pass".
```
**Look for:** the units (see TRANSCRIPT) — D_ℓ vs C_ℓ and μK vs K. `python scripts/cmb.py --help` works.

### Step 4 — Explore + weave (the units trap)
```
Create notebook.ipynb: load the real Planck TT, plot it, then DELIBERATELY plot raw C_ℓ to
show it looks nothing like the data, then the correctly normalized D_ℓ. Then fit (importing
fit_cosmology) and print parameters vs Planck. Commit "step 4: notebook".
```
**Look for:** the notebook *shows* the wrong-units curve before the right one — that contrast
is the lesson.

### Step 5 — Inspect the fit (TT and TE)
```
Write scripts/make_figures.py: fit the real data, cache results/best_fit.json, and save
results/tt_fit.png and results/te_fit.png (data + best-fit theory + residual panels). Look:
does ONE set of parameters track BOTH spectra, and are the residuals consistent with the
error bars? Commit "step 5: figures".
```
**Look for:** the same best fit on TT *and* TE, residuals scattered around zero within ±1σ.
A good TT fit that misses TE means a bug or a too-simple model.

### Step 6 — Real Planck + the Hubble tension
```
Report H0, ωc, As vs Planck 2018 and χ²/dof. Then compare this early-Universe H0 to demo
05_hubble's local H0 = 74.8 and explain the Hubble tension. State the simplifications.
Commit "step 6: real Planck result".
```
**Look for:** ~67 / 0.120 / 2.10, χ²/dof ≈ 1.1, and an honest framing of the tension and the
caveats — no overclaiming a Planck-grade measurement.

### Step 7 — Notes
```
Write notes/NOTES_cmb.md (decisions, the FULL list of simplifications, the units gotcha, the
ESA PLA data source) and notes/HANDOFF_cmb.md. Commit "step 7: notes".
```
**Look for:** the simplifications are written down, not buried. That honesty is the grade.

---
`git tag` lists `07-cmb-step-1 … -step-7`.
```
git diff 07-cmb-step-3 -- 07_cmb_power_spectrum/project/scripts/cmb.py
```
