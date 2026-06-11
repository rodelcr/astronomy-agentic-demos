# Plan — Exoplanet transit fit (Kepler-8 b)

> The design doc, written before any code. In Claude Code this is your plan-mode
> output. `walkthrough/PROMPTS.md` is this plan executed; `project/` is the result.

## Context

When a planet crosses in front of its star, the star dims by a fraction equal to
the planet-to-star area ratio. Measure that dip and you measure the planet's size.
This is *the* workhorse of exoplanet science (Kepler, TESS, JWST). The student
measures the radius ratio **Rp/R★** for **Kepler-8 b**, a hot Jupiter, from a real
Kepler light curve — and learns to trust the number only after it survives a known
synthetic answer and agreement with the gold-standard transit code `batman`.

## The science (what we're measuring)

- **Input data:** one quarter of real Kepler long-cadence photometry of Kepler-8
  (KIC 6922244), plus a seeded synthetic light curve with a *known* injected depth.
- **Method:** phase-fold the light curve at the known period, then fit a simple
  **trapezoid** transit model (flat bottom + linear ingress/egress) to the folded
  curve. The fitted depth δ gives the radius ratio.
- **Key relation:** for a uniformly bright star, fractional depth `δ = (Rp/R★)²`,
  so **Rp/R★ = √δ**. (Limb darkening deepens the real dip — discussed in the notes.)
- **Headline output:** Rp/R★ ≈ 0.094 for Kepler-8 b (literature: 0.094, Jenkins
  et al. 2010).
- **External answer key:** `batman` (Mandel & Agol 2002 model) — the community
  standard transit-light-curve code.

## Approach (and the alternative we rejected)

- **Chosen:** fit a 4-parameter **trapezoid** (depth, flat half-width, total
  half-width, center) with `scipy.optimize.curve_fit`. Few parameters, robust,
  and the depth maps directly to a radius — ideal for an undergrad's first fit.
- **Rejected:** fitting the full Mandel–Agol model with limb-darkening coefficients
  ourselves. More "correct" but it buries the one idea (depth → radius) under
  numerics and degeneracies. We instead *validate against* that model via `batman`.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | seeded trapezoid+noise light curve + `params.json` truth |
| `data/real/kepler8_q3.csv` | real Kepler-8 quarter (time, flux, flux_err), median-normalized |
| `scripts/transit.py` | `phase_fold`, `fit_transit`, `rp_over_rstar`; importable + CLI |
| `tests/test_transit.py` | (a) recover injected depth; (b) agree with `batman` |
| `notebook.ipynb` | explore the real curve, fold it, fit, inspect residuals |
| `results/` | `folded_fit.png`, `residuals.png` |
| `notes/` | NOTES + HANDOFF |

## Build steps

Steps 1–9 of `walkthrough/PROMPTS.md`, each a commit + `01-transit-step-N` tag:
failing recovery test → synthetic data → notebook fold → diagnose residuals →
refactor to `transit.py`+CLI (recovery test green) → tidy → `batman` agreement test
→ run on real Kepler-8 → notes.

## Verification

- `pytest` green: synthetic recovery **and** `batman` agreement.
- `python scripts/transit.py --data data/real/kepler8_q3.csv --period 3.52254
  --t0 <bkjd> --help` works.
- `notebook.ipynb` runs headless.
- `results/folded_fit.png` shows a clean trapezoid through the folded transit with
  structureless residuals.

## Risks / notes

- **Limb darkening:** real mid-transit dip is deeper than (Rp/R★)², so √δ slightly
  *over*estimates Rp/R★. The `batman` hard test therefore uses a **uniform source**
  (no limb darkening) where δ = (Rp/R★)² exactly; the limb-darkened case is shown
  in the notebook as a teaching caveat, not asserted.
- Real Kepler flux has stellar variability/residual trends; we fold on the known
  period and fit only near the transit to keep the trapezoid valid.
