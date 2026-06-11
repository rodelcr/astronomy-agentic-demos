# HANDOFF — period demo

**TL;DR.** Found the pulsation period of the classical Cepheid **V1154 Cyg** from a
real Kepler quarter using the string-length method, cross-checked against
Lomb-Scargle:

> **P = 4.925 d** (literature 4.9254 d) — two independent methods agree to 0.3%.
> Leavitt law → distance ~2.6 kpc (scaffolded illustration).

## What's here

| File | What it is |
|------|-----------|
| `scripts/variable.py` | `string_length_period`, `phase_fold`, `lombscargle_period` + CLI |
| `scripts/make_figures.py` | regenerates `results/periodogram.png`, `results/folded.png` |
| `tests/test_variable.py` | injected-period recovery + Lomb-Scargle agreement |
| `data/real/v1154cyg_q3.csv` | real Kepler V1154 Cyg quarter (SAP, relative mag) |
| `data/synthetic/` | seeded Fourier-Cepheid + `params.json` |
| `notebook.ipynb` | exploration → period → fold → distance |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest
python scripts/make_figures.py
python scripts/variable.py --data data/real/v1154cyg_q3.csv --pmin 3 --pmax 7
```

## Validation status

- ✅ Recovers injected synthetic period (1% tol).
- ✅ String-length ≈ Lomb-Scargle (0.26% on real data).
- ✅ Within 0.3% of literature period.

## Outstanding / extensions

- Coarse→fine period refinement (and a sub-sample parabolic peak fit) for sharper P.
- Propagate an uncertainty on P (e.g. bootstrap the epochs).
- Fit the full P–L relation across several Cepheids instead of one literature M_V.
