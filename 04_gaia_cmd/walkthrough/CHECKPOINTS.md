# Checkpoint tags — Gaia CMD

```bash
git checkout 04-gaia-step-3      # right after the distance estimator passed
git diff   04-gaia-step-3 -- 04_gaia_cmd/project/scripts/cluster.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `04-gaia-step-1` | two failing tests (distance recovery + astropy conversion) vs a stub |
| `04-gaia-step-2` | seeded synthetic cluster at a known distance + `params.json` |
| `04-gaia-step-3` | `scripts/cluster.py` implemented; **both tests green** + CLI |
| `04-gaia-step-4` | `notebook.ipynb` (naive vs robust distance + CMD) |
| `04-gaia-step-5` | `make_figures.py` + `results/` CMD & parallax histogram |
| `04-gaia-step-6` | real Pleiades distance + literature check |
| `04-gaia-step-7` | `notes/` NOTES (with the ADQL query) + HANDOFF |

> The 1/parallax bias caught inside step 3 is described in `TRANSCRIPT.md`.
