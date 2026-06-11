# Prompt walkthrough — period of a Cepheid

The agentic-coding side. Paste each step into Claude Code in your own empty folder,
one at a time; read the diff and look at the output before continuing. Compare your
work against `../project/` and the tags in `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 02_period_luminosity/PLAN.md and project/README.md. What are we measuring, with
what method, and what independent library do we validate against? No code yet.
```
**Look for:** "period via string-length, validated against Lomb-Scargle." The word
*independent* is the point — make sure it understands why we don't test LS vs LS.

### Step 1 — Tests first (red)
```
Write tests/test_variable.py with two tests, plus a stub scripts/variable.py so they
import and fail:
  1. test_recovers_injected_period — fit synthetic data (made next), assert we get the
     injected period.
  2. test_agrees_with_lombscargle — assert our string-length period matches astropy's
     Lomb-Scargle on the same data within 1%.
Run pytest, show me red. Commit "step 1: failing tests".
```
**Look for:** failure for the right reason (stub / no data).

### Step 2 — Synthetic data with a known period
```
Write data/synthetic/make_synthetic.py: a seeded, UNEVENLY sampled Cepheid-like light
curve (sum of a few Fourier harmonics for an asymmetric shape) with a known period +
noise. Write lightcurve.csv (time,mag,mag_err) and params.json. Run it.
Commit "step 2: synthetic data + ground truth".
```
**Look for:** uneven sampling on purpose — even sampling makes period-finding too easy.

### Step 3 — Implement the period finder (green)
```
Implement scripts/variable.py: phase_fold(time, period); string_length_period(...)
that, over a grid of trial periods, folds, sorts by phase, and minimizes the summed
connecting-line length (normalize the mag axis by its range so both axes matter!);
lombscargle_period(...) wrapping astropy. Make both tests pass; add a CLI.
Commit "step 3: string-length finder passes both tests".
```
**Look for:** the normalization gotcha (see TRANSCRIPT) — without it the minimum is
shallow and the period is noisy. `python scripts/variable.py --help` works.

### Step 4 — Explore + weave in the notebook
```
Create notebook.ipynb: load data/real/v1154cyg_q3.csv, plot it, find the period with
BOTH methods (importing from scripts/variable.py), fold, and add a scaffolded
Leavitt-law distance step. Commit "step 4: notebook".
```
**Look for:** the notebook imports the script's functions; both methods printed side
by side.

### Step 5 — Inspect
```
Write scripts/make_figures.py for results/periodogram.png (string-length curve with
both methods' best periods marked) and results/folded.png. Look at folded.png: does
it show one clean asymmetric cycle? If it's smeared, the period is wrong.
Commit "step 5: figures".
```
**Look for:** a crisp fast-rise/slow-decline Cepheid fold. Smearing = wrong period or
a normalization bug.

### Step 6 — Real star + literature check
```
Report the period for V1154 Cyg from both methods, compare to literature 4.9254 d,
and explain the small SAP-trend-driven difference between the two methods.
Commit "step 6: real V1154 Cyg result".
```
**Look for:** ~4.925 d, methods agreeing to a few tenths of a percent.

### Step 7 — Notes
```
Write notes/NOTES_period.md (decisions + the mag-normalization gotcha) and
notes/HANDOFF_period.md (headline P, files, reproduce, extensions).
Commit "step 7: notes".
```
**Look for:** reproducible from the HANDOFF alone.

---
`git tag` lists `02-period-step-1 … -step-7`. Diff vs the reference:
```
git diff 02-period-step-3 -- 02_period_luminosity/project/scripts/variable.py
```
