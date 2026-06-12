# Prompt walkthrough — blackbody fit (CMB temperature)

The agentic-coding side. Paste each step into Claude Code in your own empty folder,
one at a time; read the diff and look at the output before continuing. Compare against
`../project/` and `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 06_blackbody/PLAN.md and project/README.md. What are we measuring, how, and what
do we validate the Planck function against? Why is the fit a single parameter? No code.
```
**Look for:** "fit absolute Planck law (one parameter T), validated against
astropy.modeling.BlackBody." The single-parameter point matters — the data are calibrated.

### Step 1 — Tests first (red)
```
Write tests/test_blackbody.py + a stub scripts/blackbody.py so they fail:
  1. test_recovers_injected_temperature — fit a synthetic blackbody of known T, recover it.
  2. test_planck_matches_astropy — assert our planck function matches
     astropy.modeling.BlackBody in ABSOLUTE units (not just shape).
Run pytest, show red. Commit "step 1: failing tests".
```
**Look for:** the astropy check is *absolute* — that's what will catch a units error.

### Step 2 — Synthetic blackbody with a known T
```
Write data/synthetic/make_synthetic.py: a Planck spectrum at a chosen T sampled at
FIRAS-like frequencies, plus noise, seeded. Save spectrum.csv + params.json. Run it.
Commit "step 2: synthetic + truth".
```
**Look for:** it imports the real planck function — so it can't run until step 3 (that's
fine; generate it after, or stub-generate then regenerate).

### Step 3 — Implement (green)
```
Implement scripts/blackbody.py: planck_MJy(freq_icm, T) returning B_ν in MJy/sr (mind
the unit conversion from cm^-1 and from CGS radiance to MJy/sr!); fit_temperature via
scipy curve_fit (one parameter). Make both tests pass; add a CLI. Commit "step 3: passes".
```
**Look for:** units (see TRANSCRIPT) — a CGS-vs-MJy slip is ~17 orders of magnitude and
breaks the fit. `--help` works.

### Step 4 — Explore + weave
```
Create notebook.ipynb: load data/real/firas_cmb.csv, plot it, fit T (importing
fit_temperature), cross-check the Planck function against astropy, and plot residuals.
Commit "step 4: notebook".
```
**Look for:** the notebook imports the script's functions; astropy and ours agree.

### Step 5 — Inspect
```
Write scripts/make_figures.py: results/firas_fit.png (data + Planck curve, error bars
magnified so they're visible) and results/residuals.png. Look: do the points sit on the
curve and are the residuals flat? Commit "step 5: figures".
```
**Look for:** points ON the curve even with errors ×400 — that flatness IS the result.

### Step 6 — Real CMB + literature
```
Report T from FIRAS and compare to 2.72548 K (Fixsen 2009). Note that the residuals are
< 0.01% — the CMB is a near-perfect blackbody. Commit "step 6: real CMB".
```
**Look for:** 2.725 K. If you get 2.7×10^something, it's the units bug.

### Step 7 — Notes
```
Write notes/NOTES_blackbody.md (decisions + the units gotcha + the LAMBDA data source)
and notes/HANDOFF_blackbody.md. Commit "step 7: notes".
```

---
`git tag` lists `06-blackbody-step-1 … -step-7`.
```
git diff 06-blackbody-step-3 -- 06_blackbody/project/scripts/blackbody.py
```
