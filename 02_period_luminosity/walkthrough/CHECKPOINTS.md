# Checkpoint tags — period of a Cepheid

```bash
git checkout 02-period-step-3      # right after the period finder passed
git diff   02-period-step-3 -- 02_period_luminosity/project/scripts/variable.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `02-period-step-1` | two failing tests (recovery + Lomb-Scargle) against a stub |
| `02-period-step-2` | seeded uneven-sampled synthetic Cepheid + `params.json` |
| `02-period-step-3` | `scripts/variable.py` implemented; **both tests green** + CLI |
| `02-period-step-4` | `notebook.ipynb` (both methods + Leavitt distance) |
| `02-period-step-5` | `make_figures.py` + `results/` periodogram & fold |
| `02-period-step-6` | real V1154 Cyg result + literature check |
| `02-period-step-7` | `notes/` NOTES + HANDOFF |

> The mag-normalization bug fixed inside step 3 is described in `TRANSCRIPT.md`.
