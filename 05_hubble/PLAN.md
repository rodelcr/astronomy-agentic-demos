# Plan — Hubble's law / H₀

> Design doc, written before code. `walkthrough/PROMPTS.md` executes it.

## Context

Galaxies recede at velocities proportional to their distance, v = H₀ d — the
observational signature of cosmic expansion. The slope, the **Hubble constant** H₀,
sets the expansion rate and (inverse) age of the Universe. The student measures H₀ from
a real galaxy sample, fitting a line through the origin and — crucially — attaching a
**bootstrap** uncertainty. The defining skills are linear regression and *honest error
bars*, validated against `scipy` and against synthetic data with a known H₀.

## The science (what we're measuring)

- **Input data:** ~600 real galaxies from Cosmicflows-3 (distance Mpc, CMB-frame
  velocity km/s); plus a synthetic Hubble diagram with a known H₀ and peculiar-velocity
  scatter.
- **Method:** through-origin least squares, H₀ = Σ(d·v)/Σ(d²); **bootstrap** the
  galaxies for a confidence interval.
- **Headline output:** H₀ ≈ 75 km/s/Mpc (consistent with local distance-ladder values;
  cf. Planck 67.4 — the "Hubble tension").
- **External answer key:** `scipy.optimize.curve_fit` of v = H₀·d (closed form vs optimizer).

## Approach (and the alternative we rejected)

- **Chosen:** through-origin fit + bootstrap CI. The bootstrap makes the error bar
  *empirical* and visible (a histogram), which is the pedagogical point.
- **Rejected:** a free-intercept `linregress`. The intercept is physically zero, and a
  spurious offset would bias the slope; we note the intercept-fit as a diagnostic, not
  the headline.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | Hubble flow at known H₀ + peculiar-velocity scatter + `params.json` |
| `data/real/cosmicflows3.csv` | cached real Cosmicflows-3 distances & velocities |
| `scripts/hubble.py` | `fit_h0`, `bootstrap_h0`; CLI |
| `tests/test_hubble.py` | recover injected H₀ (+ interval brackets truth); match scipy |
| `notebook.ipynb` | diagram → fit → scipy cross-check → bootstrap |
| `results/` | `hubble_diagram.png`, `bootstrap.png` |
| `notes/` | NOTES (incl. the VizieR source) + HANDOFF |

## Verification

- `pytest` green: injected-H₀ recovery **and** bootstrap interval brackets the truth
  **and** scipy agreement (1e-6).
- `python scripts/hubble.py --data data/real/cosmicflows3.csv` prints H₀ ± error.
- `results/hubble_diagram.png` shows a clear linear trend through the origin.

## Risks / notes

- **Peculiar velocities** dominate scatter at small distances; we cut to Vcmb > 500 km/s
  and 10–200 Mpc so the Hubble flow is clean. Document the cuts — they shift H₀.
- The bootstrap statistical error is small (~1 km/s/Mpc); the *real* H₀ debate is about
  systematics (distance calibration), which a bootstrap does **not** capture — say so.
