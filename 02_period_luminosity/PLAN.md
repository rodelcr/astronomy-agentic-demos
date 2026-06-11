# Plan — Period of a Cepheid (V1154 Cyg)

> Design doc, written before code (your plan-mode output). `walkthrough/PROMPTS.md`
> executes this; `project/` is the result.

## Context

A pulsating variable star's period is the key that unlocks its distance: the
period–luminosity (Leavitt) law turns an easily-measured period into an intrinsic
luminosity, and thus a distance — the first rung of the cosmic distance ladder. The
student finds the pulsation **period** of **V1154 Cyg**, the only classical Cepheid
in the Kepler field, from a real light curve, using a method (**string length**)
that is *architecturally independent* of the `astropy` Lomb-Scargle reference. Two
unrelated methods agreeing is the lesson.

## The science (what we're measuring)

- **Input data:** one quarter of real Kepler photometry of V1154 Cyg (KIC 7548061),
  as relative magnitudes; plus a seeded synthetic light curve with a known period.
- **Method:** **string-length minimization** (Dworetsky 1983) — for each trial
  period, fold, sort by phase, sum the connecting line length; the period that
  stacks the points tightest wins.
- **Headline output:** P = 4.925 d (literature 4.9254 d).
- **External answer key:** `astropy.timeseries.LombScargle` — a completely different
  (Fourier-based) period finder. Agreement ≠ coincidence.
- **Coda (scaffolded):** the Leavitt law turns P into M_V and, with the apparent
  magnitude, a distance of a few kpc.

## Approach (and the alternative we rejected)

- **Chosen:** implement string-length ourselves and *validate against* Lomb-Scargle.
  This gives a genuine cross-check between independent estimators.
- **Rejected:** implementing Lomb-Scargle ourselves and testing against astropy's
  Lomb-Scargle — that's circular (same method twice). Independence is the point.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | seeded Fourier-series Cepheid + uneven sampling + `params.json` |
| `data/real/v1154cyg_q3.csv` | real Kepler V1154 Cyg quarter (time, mag, mag_err) |
| `scripts/variable.py` | `string_length_period`, `phase_fold`, `lombscargle_period`; CLI |
| `tests/test_variable.py` | recover injected period; agree with Lomb-Scargle |
| `notebook.ipynb` | explore → period (2 methods) → fold → Leavitt distance |
| `results/` | `periodogram.png`, `folded.png` |
| `notes/` | NOTES + HANDOFF |

## Verification

- `pytest` green: injected-period recovery **and** string-length ≈ Lomb-Scargle (1% tol).
- `python scripts/variable.py --data data/real/v1154cyg_q3.csv --pmin 3 --pmax 7` runs.
- `results/folded.png` shows a clean asymmetric Cepheid pulsation.

## Risks / notes

- **SAP vs PDCSAP:** we use SAP flux to preserve the intrinsic pulsation (PDC can
  suppress real long-timescale variability). Residual instrumental trends shift the
  Lomb-Scargle peak ~0.2%, hence the ~0.26% method-to-method difference — honest and
  worth showing.
- String-length over N trial periods is an O(N · n log n) brute scan; 8000 trials on
  ~4000 points runs in ~1 s. Fine for a demo; mention coarse→fine refinement as an
  extension.
