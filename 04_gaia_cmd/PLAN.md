# Plan — Gaia color–magnitude diagram (Pleiades)

> Design doc, written before code. `walkthrough/PROMPTS.md` executes it.

## Context

A color–magnitude diagram (CMD) is a cluster's H–R diagram: plot every star's color
against its absolute magnitude and a single-age cluster traces a tight main sequence.
Building one requires a **distance** (to turn apparent into absolute magnitude), which
Gaia gives via **parallax**. The student queries real Gaia data for the **Pleiades**,
measures its distance, and makes the CMD — learning that 1/parallax is a *biased*
distance estimator when parallaxes are noisy.

## The science (what we're measuring)

- **Input data:** a cached Gaia DR3 query of ~1000 Pleiades members (parallax, G, BP−RP,
  proper motions); plus a synthetic cluster at a known distance with noisy parallaxes.
- **Method:** inverse-variance-weighted **mean parallax**, inverted once → distance;
  absolute magnitude M_G = G + 5 + 5 log₁₀(ϖ/1000); CMD = M_G vs BP−RP.
- **Headline output:** Pleiades distance ≈ 136 pc (literature 136.2 pc).
- **External answer key:** `astropy.coordinates.Distance` for the parallax→distance
  conversion (unit-aware, standard).

## Approach (and the alternative we rejected)

- **Chosen:** average parallax then invert — unbiased for a common-distance cluster.
- **Rejected:** average per-star 1/ϖ — biased when ϖ is noisy (the nonlinear transform
  inflates the mean distance). The demo demonstrates the difference rather than hiding it.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | cluster at a known distance + noisy parallaxes + `params.json` |
| `data/real/pleiades_gaia.csv` | cached real Gaia DR3 Pleiades members |
| `scripts/cluster.py` | `parallax_to_distance`, `cluster_distance`, `absolute_magnitude`; CLI |
| `tests/test_cluster.py` | recover injected distance; conversion matches astropy |
| `notebook.ipynb` | distance (naive vs robust) → CMD → astropy cross-check |
| `results/` | `cmd.png`, `parallax_hist.png` |
| `notes/` | NOTES (incl. the exact ADQL query) + HANDOFF |

## Verification

- `pytest` green: injected-distance recovery (1%) **and** astropy conversion match (1e-6).
- `python scripts/cluster.py --data data/real/pleiades_gaia.csv` prints ~136 pc.
- `results/cmd.png` shows a tight main sequence.

## Risks / notes

- **Offline:** the live Gaia query is flaky in class, so we cache the result as CSV and
  ship it; the ADQL is recorded in `notes/` so the query is reproducible.
- **Membership:** we pre-filter by parallax and proper motion to isolate real members;
  loose cuts add field-star scatter to the CMD (visible in the figure as off-sequence
  points). Faint red end naturally broadens (binaries + larger errors).
