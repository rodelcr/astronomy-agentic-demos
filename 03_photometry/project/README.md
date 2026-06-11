# Aperture photometry — measuring star brightnesses in M67

## The problem

How bright is a star in an image? Add up its light. The catch is *which* light is the
star and which is the sky. **Aperture photometry** answers it: sum the pixels in a
circle centered on the star (the **aperture**), and subtract a sky level estimated
from a surrounding ring (the **annulus**). Here we do this on a real CCD image of the
open cluster **M67**.

## Physics scaffold

A star's measured signal in an aperture is

> **net counts = Σ(aperture pixels) − sky_per_pixel × N_aperture**

where `sky_per_pixel` is the median of the annulus pixels (median, so a stray star in
the ring doesn't bias it). Brightness in magnitudes is

> **m = ZP − 2.5 log₁₀(net counts)**

The zero point ZP just sets the scale; without standard stars it's arbitrary, so we
report *instrumental* magnitudes and trust **differences** between stars.

> Headline result: our hand-rolled photometry reproduces `photutils` **exactly**
> (max fractional difference 0) on the real M67 image, and recovers known relative
> magnitudes to 0.02 mag on synthetic stars.

## What's in here

```
project/
  notebook.ipynb         view → detect → measure → cross-check → inspect apertures
  scripts/photometry.py  aperture_flux, instrumental_mag, measure — importable + CLI
  tests/test_photometry.py  relative-photometry recovery + exact photutils agreement
  data/
    real/m67_cutout.fits     real Palomar Schmidt M67 cutout
    synthetic/               make_synthetic.py + params.json (known fluxes)
  results/               apertures.png, compare.png
  notes/                 NOTES + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/photometry.py --image data/real/m67_cutout.fits --nbright 10
```

## External answer key

Validated against **`photutils.aperture`** — see
`tests/test_photometry.py::test_agrees_with_photutils`.

## Data provenance

`data/real/m67_cutout.fits` is a 400×400 cutout of a **real** Palomar 48-inch Schmidt
CCD image of M67, distributed as a sample image with `photutils` and re-saved here as
a standalone FITS (so the demo doesn't depend on a deprecated loader). Header keywords
record the origin. Nothing is fabricated.
