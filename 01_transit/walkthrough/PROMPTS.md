# Prompt walkthrough — transit fit (Kepler-8 b)

The agentic-coding side. Paste each step into Claude Code *in your own empty
folder*, one at a time, and read the diff / look at the output before continuing.
Driving the agent step by step **is** the skill. Compare your result against the
reference in `../project/` and the checkpoint tags in `CHECKPOINTS.md`.

> The arc is: **tests first → data → implement → explore → inspect → real data →
> notes.** Seven commits, one per step.

---

### Step 0 — Orient
```
Read 01_transit/PLAN.md and project/README.md. In your own words: what are we
measuring, from what data, and what external library do we validate against?
No code yet.
```
**Look for:** "Rp/R★ from transit depth, validated against batman." If it can't say
that, the plan isn't clear enough yet.

### Step 1 — Tests first (TDD red)
```
Write tests/test_transit.py with TWO tests, then a stub scripts/transit.py so they
import but fail:
  1. test_recovers_injected_depth: load data/synthetic/{lightcurve.csv,params.json}
     (we'll make them next), fit, and assert we recover the injected depth & Rp/R*.
  2. test_agrees_with_batman: build a UNIFORM-source transit with batman for a known
     rp, run our fit, assert we recover rp within 3%.
Run pytest and show me the red output. Commit "step 1: failing tests".
```
**Look for:** failures from `NotImplementedError` / missing data — the *right* reasons.

### Step 2 — Synthetic data with a known answer
```
Write data/synthetic/make_synthetic.py: a seeded trapezoid transit (flat bottom +
linear ingress/egress) repeated over ~27 days with Gaussian noise. Write
lightcurve.csv (time,flux,flux_err) and params.json with the true depth, period,
t0, durations. Run it. Commit "step 2: synthetic data + ground truth".
```
**Look for:** open `params.json` — depth 0.01, Rp/R★ 0.10. That's your oracle.

### Step 3 — Implement the estimator (TDD green)
```
Implement scripts/transit.py: phase_fold(time, period, t0) -> phase in [-0.5,0.5);
fit_transit(...) that folds, keeps |phase|<window, and fits a trapezoid with
scipy.optimize.curve_fit; rp_over_rstar(depth)=sqrt(depth). Make both tests pass.
Add an argparse CLI. Commit "step 3: estimator passes both tests".
```
**Look for:** green — and watch the phase convention (see the transcript; an
off-by-half-period bug here is classic). `python scripts/transit.py --help` works.

### Step 4 — Explore + weave in the notebook
```
Create notebook.ipynb that loads the real curve data/real/kepler8_q3.csv, plots it,
folds it on P=3.52254 d, and IMPORTS fit_transit from scripts/transit.py to fit it
(don't re-implement in the notebook). Show depth -> Rp/R*. Commit "step 4: notebook".
```
**Look for:** the notebook *calls* the script's function. Notebooks think; scripts
are trusted. That's the weave.

### Step 5 — Inspect the residuals
```
Write scripts/make_figures.py to save results/folded_fit.png (folded transit +
trapezoid fit, with a residual panel beneath) and results/residuals.png (residual
histogram). Then look at folded_fit.png and tell me honestly: is there structure in
the residuals? What causes any leftover dip at mid-transit? Commit "step 5: figures".
```
**Look for:** the faint mid-transit residual is **limb darkening** — make the agent
name it, not hand-wave. This is the habit that separates a fit from a result.

### Step 6 — Run on the real planet
```
Run the fit on data/real/kepler8_q3.csv (P=3.52254 d, t0 from a BoxLeastSquares
search). Compare Rp/R* to the literature 0.0944 and note the small offset's cause.
Commit "step 6: real Kepler-8 result".
```
**Look for:** ~0.094, within ~1% of literature. Real data is messier than synthetic
— expect and explain the small gap.

### Step 7 — Notes
```
Write notes/NOTES_transit.md (decisions + the phase-fold dead end) and
notes/HANDOFF_transit.md (headline Rp/R* ± context, files, how to reproduce,
extensions). Commit "step 7: notes".
```
**Look for:** could a labmate reproduce the result from the HANDOFF alone? That's the bar.

---

`git log --oneline` should now read like these steps; `git tag` lists
`01-transit-step-1 … -step-7`. Diff yours against the reference:
```
git diff 01-transit-step-3 -- 01_transit/project/scripts/transit.py
```
