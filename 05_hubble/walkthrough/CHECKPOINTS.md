# Checkpoint tags — Hubble's law

```bash
git checkout 05-hubble-step-3      # right after fit + bootstrap passed
git diff   05-hubble-step-3 -- 05_hubble/project/scripts/hubble.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `05-hubble-step-1` | two failing tests (H₀ recovery + scipy match) against a stub |
| `05-hubble-step-2` | seeded synthetic Hubble flow at known H₀ + `params.json` |
| `05-hubble-step-3` | `scripts/hubble.py` implemented; **both tests green** + CLI |
| `05-hubble-step-4` | `notebook.ipynb` (diagram → fit → scipy → bootstrap) |
| `05-hubble-step-5` | `make_figures.py` + `results/` Hubble diagram & bootstrap |
| `05-hubble-step-6` | real Cosmicflows-3 H₀ + tension context |
| `05-hubble-step-7` | `notes/` NOTES (with source/cuts) + HANDOFF |

> The free-intercept-vs-through-origin mistake fixed inside step 3 is in `TRANSCRIPT.md`.
