# Prompt walkthrough — <demo title>

This is the **agentic-coding side** of the demo. Each numbered step is a prompt
you paste into Claude Code (in your own empty working folder), plus a note on
**what to look for** before moving on. The steps deliberately rehearse the five
habits (notes, version control, plot inspection, notebook↔script, testing).

> Tip: don't paste all nine at once. Run one, read the diff, look at the output,
> *then* continue. Driving the agent step by step is the whole skill.

---

### Step 0 — Orient the agent
```
Read the project README and tell me, in your own words, what we're measuring,
what data we have, and what external library we'll check our answer against.
Don't write any code yet.
```
**Look for:** does it correctly identify the headline quantity and the answer-key
library? If not, your README is unclear — fix that first.

### Step 1 — Repo + a failing test (TDD red)
```
Initialize a git repo. Create scripts/<name>.py with a stub function that returns
None, and tests/test_<name>.py with one test that asserts the function recovers a
known injected value (we'll generate that data next). Run pytest and show me the
failing output. Commit as "step 1: failing test".
```
**Look for:** the test *fails for the right reason* (stub returns None), not an
import error. A red test you understand is the foundation.

### Step 2 — Synthetic data with a known answer
```
Write data/synthetic/make_synthetic.py: generate <data> from explicit parameters
with a FIXED random seed, write the array to disk, and write params.json with the
ground-truth values. Run it. Commit as "step 2: synthetic data + ground truth".
```
**Look for:** open `params.json`. These numbers are your test oracle — the test
passes only if your code recovers them.

### Step 3 — Explore in the notebook
```
In notebook.ipynb, load the synthetic data and plot it. Then prototype the
measurement in cells — rough and interactive is fine. Save your exploratory plot
to results/.
```
**Look for:** *you* look at the plot. Does the signal look like what the physics
says it should? This is where intuition is built.

### Step 4 — Inspect and iterate on the figure
```
Look at results/<figure>.png and tell me honestly whether the fit is good. Are
there systematic trends in the residuals? If so, what's the likely cause, and fix
it. Re-save the figure.
```
**Look for:** structure in residuals = something is wrong. Make the agent diagnose
before it "improves." This is the most important habit and the easiest to skip.

### Step 5 — Refactor notebook → script (weaving)
```
Move the working measurement out of the notebook into scripts/<name>.py as a
clean importable function with a docstring AND an argparse __main__ CLI
(so `python scripts/<name>.py --data ...` works). Then import that function back
into the notebook to confirm it gives the same result. Commit as "step 5: refactor
to script".
```
**Look for:** `python scripts/<name>.py --help` works, and the notebook now *calls*
the function instead of redefining it. Notebooks think; scripts are trusted.

### Step 6 — Make the synthetic test pass (TDD green)
```
Now make the test from step 1 pass: it should call the real function and assert it
recovers the injected value from params.json within a sensible tolerance. Run
pytest. Commit as "step 6: synthetic recovery passes".
```
**Look for:** green — and a tolerance you can justify, not one fudged to pass.

### Step 7 — Validate against the external library (the defining habit)
```
Add a second test that runs <library> on the SAME data and asserts our result
agrees with it within tolerance. Explain why <library> is a trustworthy reference.
Run pytest. Commit as "step 7: external-library agreement".
```
**Look for:** two independent confirmations now back the number — a known answer
and a community-validated tool. *That's* a result you can believe.

### Step 8 — Run on the real data
```
Run the script on data/real/. Compare the result to the literature value in the
README. Save the final phase-folded / fit figure to results/. Commit + tag this
checkpoint.
```
**Look for:** the real-data answer is in the right ballpark of the literature
value. Real data is messier than synthetic — expect a small discrepancy and say so.

### Step 9 — Write the notes
```
Write notes/NOTES_<name>.md (what we tried, dead ends, decisions) and
notes/HANDOFF_<name>.md (TL;DR with the headline number ± error, files changed,
caches on disk, what's left to do). Commit as "step 9: notes".
```
**Look for:** could a labmate (or you, in a month) pick this up from the HANDOFF
alone? That's the bar.

---

When you're done, `git log --oneline` should read like the steps above, and
`git tag` should list your checkpoints. Compare against the reference in
`../project/` and the tag map in `CHECKPOINTS.md`.
