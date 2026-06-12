# Prompt walkthrough — Gaia color–magnitude diagram

The agentic-coding side. Paste each step into Claude Code in your own empty folder,
one at a time; read the diff and look at the output before continuing. Compare against
`../project/` and `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 04_gaia_cmd/PLAN.md and project/README.md. What are we measuring, with what
method, and what library do we validate the parallax→distance conversion against? No code.
```
**Look for:** "cluster distance from mean parallax, validated against astropy.Distance."

### Step 1 — Tests first (red)
```
Write tests/test_cluster.py + a stub scripts/cluster.py so they import and fail:
  1. test_recovers_injected_distance — synthetic cluster at a known distance with noisy
     parallaxes; assert our estimator recovers it.
  2. test_conversion_matches_astropy — assert parallax_to_distance matches
     astropy.coordinates.Distance(parallax=...).
Run pytest, show red. Commit "step 1: failing tests".
```
**Look for:** make the agent explain why a noisy cluster is the right test — it's where
the 1/parallax bias bites.

### Step 2 — Synthetic cluster with a known distance
```
Write data/synthetic/make_synthetic.py: N stars at ONE true distance, with Gaia-like
parallax noise. Save cluster.csv + params.json. Run it. Commit "step 2: synthetic + truth".
```
**Look for:** all stars share the true parallax; only noise differs.

### Step 3 — Implement (green)
```
Implement scripts/cluster.py: parallax_to_distance (1000/ϖ); cluster_distance =
inverse-variance-weighted mean parallax, inverted once (NOT mean of 1/ϖ);
absolute_magnitude. Make both tests pass; add a CLI. Commit "step 3: estimator passes".
```
**Look for:** the bias point — averaging 1/ϖ would fail the recovery test. `--help` works.

### Step 4 — Explore + weave
```
Create notebook.ipynb: load data/real/pleiades_gaia.csv, compute distance the NAIVE
way (mean of 1/ϖ) and the ROBUST way (import cluster_distance), show they differ, then
build the CMD (absolute G vs BP−RP). Commit "step 4: notebook".
```
**Look for:** both distances printed; the CMD imports the script's functions.

### Step 5 — Inspect the CMD
```
Write scripts/make_figures.py for results/cmd.png and results/parallax_hist.png. Look at
cmd.png: is the main sequence tight? Off-sequence scatter = field-star contamination
from loose membership cuts. Commit "step 5: figures".
```
**Look for:** a tight main sequence. A second blob or heavy scatter = bad membership.

### Step 6 — Real cluster + literature
```
Report the Pleiades distance and compare to literature 136.2 pc. Note the small
naive-vs-robust difference as the 1/parallax bias. Commit "step 6: real Pleiades".
```
**Look for:** ~136 pc, robust < naive.

### Step 7 — Notes
```
Write notes/NOTES_cmd.md (decisions + the EXACT ADQL query so the cache is reproducible)
and notes/HANDOFF_cmd.md. Commit "step 7: notes".
```
**Look for:** the query is recorded — a cache nobody can reproduce is a liability.

---
`git tag` lists `04-gaia-step-1 … -step-7`.
```
git diff 04-gaia-step-3 -- 04_gaia_cmd/project/scripts/cluster.py
```
