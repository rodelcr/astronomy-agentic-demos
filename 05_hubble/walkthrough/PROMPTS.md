# Prompt walkthrough — Hubble's law / H₀

The agentic-coding side. Paste each step into Claude Code in your own empty folder,
one at a time; read the diff and look at the output before continuing. Compare against
`../project/` and `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 05_hubble/PLAN.md and project/README.md. What are we measuring, how, and what do
we validate the fit against? What does the bootstrap give us — and what does it NOT? No code.
```
**Look for:** "through-origin slope, validated against scipy; bootstrap gives the
*statistical* error, not the distance-scale systematics."

### Step 1 — Tests first (red)
```
Write tests/test_hubble.py + a stub scripts/hubble.py so they fail:
  1. test_recovers_injected_H0 — fit synthetic data of known H0; assert the estimate is
     close AND the bootstrap interval brackets the truth.
  2. test_agrees_with_scipy — assert our closed-form slope matches scipy curve_fit of v=H0*d.
Run pytest, show red. Commit "step 1: failing tests".
```
**Look for:** the second assertion (interval brackets truth) — an error bar that misses
the known answer is a bug.

### Step 2 — Synthetic Hubble diagram
```
Write data/synthetic/make_synthetic.py: galaxies at random distances with v = H0*d plus
peculiar-velocity scatter, seeded. Save hubble.csv + params.json. Run it.
Commit "step 2: synthetic + truth".
```
**Look for:** scatter is peculiar velocity (km/s), independent of distance.

### Step 3 — Implement (green)
```
Implement scripts/hubble.py: fit_h0 = through-origin LS Σ(d·v)/Σ(d²); bootstrap_h0
returning (median, 16th, 84th pct) over resamples. Make both tests pass; add a CLI.
Commit "step 3: fit + bootstrap pass".
```
**Look for:** through the origin, not a free intercept. `--help` works.

### Step 4 — Explore + weave
```
Create notebook.ipynb: load data/real/cosmicflows3.csv, plot the Hubble diagram, fit H0
(importing fit_h0), cross-check vs scipy, and bootstrap the error bar. Mention the
Hubble tension. Commit "step 4: notebook".
```
**Look for:** the notebook imports the script's functions; scipy and ours agree.

### Step 5 — Inspect
```
Write scripts/make_figures.py: results/hubble_diagram.png (points + fit line through
origin) and results/bootstrap.png (histogram of refit H0 with the interval shaded).
Look: does the line pass through (0,0) and track the cloud? Commit "step 5: figures".
```
**Look for:** a line forced through the origin that still tracks the data = a real
linear law. A line that misses the origin means you fit an intercept by mistake.

### Step 6 — Real galaxies + context
```
Report H0 ± bootstrap error for the real sample, compare to Planck 67.4 and local ~73,
and state clearly what the bootstrap error does and does NOT include. Commit "step 6: real H0".
```
**Look for:** ~75 with a small statistical error; the honest caveat about systematics.

### Step 7 — Notes
```
Write notes/NOTES_hubble.md (decisions, the bootstrap caveat, the VizieR source +
cuts) and notes/HANDOFF_hubble.md. Commit "step 7: notes".
```

---
`git tag` lists `05-hubble-step-1 … -step-7`.
```
git diff 05-hubble-step-3 -- 05_hubble/project/scripts/hubble.py
```
