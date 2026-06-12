# NOTES — blackbody demo

## Decisions

- **Fit the absolute Planck law (one parameter).** The FIRAS spectrum is calibrated in
  MJy/sr, so the Planck normalization is physical — no free amplitude. T is the only
  parameter, which is the cleanest possible fit and makes the recovered number a real
  temperature, not a shape match.
- **Work in MJy/sr with frequency in cm⁻¹.** Match the data's native units; convert
  inside `planck_MJy`. The astropy cross-check guards the conversion.

## Dead end / gotcha (the wrong turn)

The first `planck_MJy` returned radiance in CGS (erg/s/cm²/Hz/sr) but the data are in
MJy/sr — a units mismatch of ~17 orders of magnitude. `curve_fit` then drove T to
absurd values (or failed to converge) trying to match the shape with the wrong scale.
The fix was the single conversion `1 MJy = 1e-17 erg/s/cm²/Hz`. The
`test_planck_matches_astropy` check (absolute, not just shape) is what pinned the units:
a shape-only comparison would have hidden the factor entirely.

## Data source (reproducible)

NASA LAMBDA: `firas_monopole_spec_v1.txt`
(`https://lambda.gsfc.nasa.gov/data/cobe/firas/monopole_spec/`). Columns used: 1
(frequency, cm⁻¹), 2 (monopole spectrum, MJy/sr), 4 (1σ uncertainty, kJy/sr → MJy/sr).
Reference: Fixsen et al. 1996, ApJ 473, 576.

## Numbers

- Synthetic injected T = 2.725 K → recovered within 1%.
- Real FIRAS: T = 2.7250 K (literature 2.72548 ± 0.00057 K). Planck function matches
  astropy.modeling.BlackBody to 1e-4 in absolute MJy/sr.
