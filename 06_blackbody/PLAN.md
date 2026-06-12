# Plan — Blackbody fit (CMB temperature)

> Design doc, written before code. `walkthrough/PROMPTS.md` executes it.

## Context

A blackbody's entire spectrum is set by one number — its temperature — through the
Planck law. Fitting that law to a measured spectrum is how we take the temperature of
stars and of the Universe itself. The student fits the Planck function to the
**COBE/FIRAS** spectrum of the cosmic microwave background, the most perfect blackbody
ever measured, and recovers **T = 2.725 K**. The estimator is validated against
`astropy.modeling.BlackBody` and against synthetic data of known temperature.

## The science (what we're measuring)

- **Input data:** the real 43-point FIRAS CMB monopole spectrum (frequency cm⁻¹,
  intensity MJy/sr, uncertainty); plus a synthetic Planck spectrum of known T.
- **Method:** `scipy.optimize.curve_fit` of B_ν(T) to the calibrated spectrum. Because
  the spectrum is absolutely calibrated, no free scale is needed — T is the only parameter.
- **Headline output:** T = 2.725 K (literature 2.72548 ± 0.00057 K, Fixsen 2009).
- **External answer key:** `astropy.modeling.BlackBody` — our Planck function must match
  it in absolute units (MJy/sr).

## Approach (and the alternative we rejected)

- **Chosen:** fit the *absolute* Planck law (one parameter, T). The data are calibrated,
  so this directly yields the physical temperature — the cleanest possible fit.
- **Rejected:** fitting shape + a free amplitude (2 parameters). Unnecessary here and it
  throws away the absolute-calibration information that makes T meaningful.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | Planck spectrum at known T + noise + `params.json` |
| `data/real/firas_cmb.csv` | real COBE/FIRAS CMB monopole spectrum |
| `scripts/blackbody.py` | `planck_MJy`, `fit_temperature`; CLI |
| `tests/test_blackbody.py` | recover injected T; Planck matches astropy |
| `notebook.ipynb` | spectrum → fit → astropy check → residuals |
| `results/` | `firas_fit.png`, `residuals.png` |
| `notes/` | NOTES (incl. data source) + HANDOFF |

## Verification

- `pytest` green: injected-T recovery (1%) **and** Planck-vs-astropy match (1e-4).
- `python scripts/blackbody.py --data data/real/firas_cmb.csv` prints ~2.725 K.
- `results/firas_fit.png` shows points on the curve; residuals flat to < 0.01%.

## Risks / notes

- **Units are the whole game.** Frequency is in cm⁻¹ (wavenumber), intensity in MJy/sr.
  The Planck constant prefactors must convert to MJy/sr exactly or the absolute fit is
  off. The astropy cross-check exists precisely to catch a units slip.
- FIRAS col2 is "2.725 K BB + residual," so the recovered T is essentially exact by
  construction; that's fine — the demo teaches the *method*, and the residual panel
  shows the (tiny) real departures from a perfect blackbody.
