# Plan — Aperture photometry (M67)

> Design doc, written before code. `walkthrough/PROMPTS.md` executes it; `project/`
> is the result.

## Context

Measuring how bright a star is in an image — **photometry** — underlies almost every
quantitative result in observational astronomy (variability, color, distance, mass).
The simplest method is the **aperture**: sum a star's light in a circle and subtract
the sky. The student implements aperture photometry by hand on a real CCD image of
the open cluster **M67** and validates it against `photutils`, the standard library —
the habit being *never trust your own pixel-summing until it matches a vetted tool*.

## The science (what we're measuring)

- **Input data:** a real 400×400 cutout of a Palomar Schmidt CCD image of M67, plus a
  seeded synthetic star field with known fluxes.
- **Method:** circular **aperture** sum minus a median **sky annulus**; instrumental
  magnitude m = ZP − 2.5 log₁₀(net counts).
- **Headline output:** our hand-rolled photometry reproduces `photutils` **exactly**
  on the real image, and recovers known relative magnitudes on synthetic stars.
- **External answer key:** `photutils.aperture` (`CircularAperture`,
  `aperture_photometry`).

## Approach (and the alternative we rejected)

- **Chosen:** a "center" aperture (count whole pixels whose center is inside the
  circle) so it maps exactly onto `photutils` `method='center'` — an exact,
  unambiguous cross-check, and the simplest thing to reason about.
- **Rejected:** fractional-pixel ("exact") apertures from scratch. More accurate, but
  the geometry obscures the lesson; we note it as the natural next step.

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | seeded Gaussian-PSF star field + `params.json` fluxes |
| `data/real/m67_cutout.fits` | real M67 CCD cutout (header: OBJECT, TELESCOP, GAIN) |
| `scripts/photometry.py` | `aperture_flux`, `aperture_flux_raw`, `instrumental_mag`, `measure`; CLI |
| `tests/test_photometry.py` | recover relative photometry; agree with photutils exactly |
| `notebook.ipynb` | view → detect → measure one star → cross-check → inspect apertures |
| `results/` | `apertures.png`, `compare.png` |
| `notes/` | NOTES + HANDOFF |

## Verification

- `pytest` green: relative-photometry recovery (0.02 mag) **and** exact photutils
  agreement (rel 1e-6).
- `python scripts/photometry.py --image data/real/m67_cutout.fits` lists star mags.
- `results/apertures.png` shows circles centered on stars with clean sky annuli.

## Risks / notes

- **Pixel-edge convention:** our mask must use strict `<` (pixel center strictly
  inside) to match `photutils method='center'`; `<=` includes a ring of edge pixels
  and breaks the exact agreement at the ~1% level. (This is the demo's "wrong turn.")
- **Crowding:** M67 is a cluster, so sky annuli can catch neighbors; the median sky
  estimate is chosen for robustness against that.
- Absolute calibration (a real zero point from standard stars) is out of scope; we
  report instrumental magnitudes and validate via agreement + relative photometry.
