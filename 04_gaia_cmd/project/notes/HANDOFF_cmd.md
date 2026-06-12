# HANDOFF — Gaia CMD demo

**TL;DR.** Measured the Pleiades distance from real Gaia parallaxes and built its
color–magnitude diagram:

> **distance = 135.9 pc** (literature 136.2 pc) from 1033 members; clean main-sequence CMD.

## What's here

| File | What it is |
|------|-----------|
| `scripts/cluster.py` | `parallax_to_distance`, `cluster_distance`, `absolute_magnitude` + CLI |
| `scripts/make_figures.py` | regenerates `results/cmd.png`, `results/parallax_hist.png` |
| `tests/test_cluster.py` | injected-distance recovery + astropy conversion match |
| `data/real/pleiades_gaia.csv` | cached real Gaia DR3 Pleiades members |
| `data/synthetic/` | seeded cluster at known distance + `params.json` |
| `notebook.ipynb` | distance (naive vs robust) → CMD → cross-check |

## Reproduce

```bash
conda activate demos
python data/synthetic/make_synthetic.py
pytest
python scripts/make_figures.py
python scripts/cluster.py --data data/real/pleiades_gaia.csv
```

## Validation status

- ✅ Recovers injected synthetic distance (1% tol).
- ✅ Parallax→distance matches astropy.coordinates.Distance (1e-6).
- ✅ Real distance within 0.2% of literature.

## Outstanding / extensions

- Overlay a theoretical isochrone (e.g. PARSEC/MIST) to read off the cluster age.
- Fit the main-sequence ridge line and de-redden.
- Propagate parallax errors into a distance uncertainty (and show the 1/ϖ bias
  quantitatively vs a proper Bayesian distance).
