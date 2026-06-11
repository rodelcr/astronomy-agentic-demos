# Checkpoint tags — transit fit

The reference `project/` was built one commit per prompt step, each marked with a
tag. Rewind to any of them, or diff your own work against them.

```bash
git checkout 01-transit-step-3      # the project right after the estimator passed
git diff   01-transit-step-3 -- 01_transit/project/scripts/transit.py
git checkout main                   # back to the finished version
```

| Tag | Captures (after this step the project has…) |
|-----|---------------------------------------------|
| `01-transit-step-1` | two failing tests (recovery + batman) against a stub |
| `01-transit-step-2` | seeded synthetic light curve + `params.json` ground truth |
| `01-transit-step-3` | `scripts/transit.py` implemented; **both tests green** + CLI |
| `01-transit-step-4` | `notebook.ipynb` exploring the real curve, importing the script |
| `01-transit-step-5` | `make_figures.py` + `results/` figures; residuals diagnosed |
| `01-transit-step-6` | run on real Kepler-8 data; README provenance + literature check |
| `01-transit-step-7` | `notes/` NOTES + HANDOFF written |

> The whole history is the story: `git log --oneline --decorate` reads like the
> seven prompt steps. The phase-fold bug fixed inside step 3 is described in
> `TRANSCRIPT.md`.
