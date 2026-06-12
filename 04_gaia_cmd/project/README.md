# Gaia color–magnitude diagram — the Pleiades

## The problem

Plot a cluster's stars by **color** (temperature) and **brightness** and they fall on
a tight curve — the main sequence — because they're all the same age and distance.
That diagram, the CMD, is the workhorse of stellar astrophysics. To make it you need a
distance, which **Gaia** provides through **parallax**. Here we use real Gaia data for
the **Pleiades**.

## Physics scaffold

Parallax ϖ (the tiny annual wobble of a nearby star) gives distance: **d [pc] = 1000 / ϖ [mas]**.
For a cluster, every star is at ~the same distance, so we average the *parallaxes*
(weighted by their errors) and invert once — *not* the per-star distances, because
1/ϖ is nonlinear and averaging it with noisy ϖ is biased.

With the distance, apparent G becomes **absolute** magnitude:

> **M_G = G + 5 + 5 log₁₀(ϖ / 1000)**

and the CMD is M_G vs the color BP − RP.

> Headline result: **Pleiades distance ≈ 136 pc** (literature 136.2 pc), with a clean
> main-sequence CMD of ~1000 members.

## What's in here

```
project/
  notebook.ipynb        distance (naive vs robust) → CMD → astropy cross-check
  scripts/cluster.py    parallax_to_distance, cluster_distance, absolute_magnitude — importable + CLI
  tests/test_cluster.py  recover injected distance + conversion matches astropy
  data/
    real/pleiades_gaia.csv   cached real Gaia DR3 query (parallax, G, BP-RP, PM)
    synthetic/               make_synthetic.py + params.json (known distance)
  results/              cmd.png, parallax_hist.png
  notes/                NOTES (incl. the ADQL query) + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/cluster.py --data data/real/pleiades_gaia.csv
```

## External answer key

The parallax→distance conversion is validated against
**`astropy.coordinates.Distance`** — see `tests/test_cluster.py::test_conversion_matches_astropy`.

## Data provenance

`data/real/pleiades_gaia.csv` is a **real** Gaia DR3 query of Pleiades members (cone
search + parallax & proper-motion cuts), cached to CSV so the demo runs offline. The
exact ADQL query is in `notes/NOTES_cmd.md`. Nothing is fabricated.
