# NOTES — CMB demo

## Decisions

- **CAMB is the model, not a hand-rolled check.** Computing a CMB spectrum from scratch
  needs a Boltzmann solver (thousands of lines, perturbation theory through recombination).
  So unlike the other demos, the external library *is* the theory engine; the student's
  contribution is the inference layer (likelihood + fit) and the normalization handling.
- **Validate the normalization, not the physics.** We can't independently check CAMB's
  physics, but we can check that *our* D_ℓ = ℓ(ℓ+1)C_ℓ/2π μK² conversion is right, against
  CAMB's raw C_ℓ converted by hand. That's the testable, student-owned piece.
- **Reduced 3-parameter fit.** {H₀, ωc, Aₛ} free; {ωb, nₛ, τ} fixed at Planck fiducial.
  These three are well constrained and reasonably separable given fixed ωb/nₛ/τ, so the
  Nelder-Mead fit is stable and recovers Planck values.

## The simplifications (be explicit — this is a teaching fit, not a Planck analysis)

1. **Likelihood:** Gaussian with *diagonal* errors on the *binned* public spectra. The real
   Planck likelihood (`plik`) uses the full bandpower covariance and ~20 foreground/
   nuisance/calibration parameters marginalized out. Consequence: our central values are
   close to Planck, but our error bars are illustrative, not official.
2. **Bandpower windows:** we sample theory at each bin's effective ℓ by interpolation. The
   correct treatment convolves theory with each bin's window function.
3. **Fixed parameters:** holding ωb, nₛ, τ fixed removes real degeneracies (e.g. As–τ). A
   full 6-parameter posterior needs MCMC (cobaya/CosmoMC), not a point optimizer.
4. **CAMB accuracy / lmax** are set for speed; production uses higher accuracy settings.

None of these are hidden: they're stated in the README and the notebook, because a fit you
can't reproduce *and bound the assumptions of* is not a measurement.

## Dead end / gotcha (the wrong turn)

The first theory overlay plotted CAMB's raw C_ℓ against the Planck D_ℓ data — and it fell
off a cliff, orders of magnitude below the peaks, looking nothing like the data. The instinct
to "rescale to match" is wrong: the issue is that the data are **D_ℓ = ℓ(ℓ+1)C_ℓ/2π in μK²**,
while raw CAMB output (with `CMB_unit=None, raw_cl=True`) is the *dimensionless* C_ℓ. The fix
is the ℓ(ℓ+1)/2π factor and the (2.7255×10⁶ μK)² scale. `test_normalization_matches_camb`
encodes exactly this and would catch it.

## Data source (reproducible)

ESA Planck Legacy Archive, via
`https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=<file>`:
`COM_PowerSpect_CMB-TT-binned_R3.01.txt` and `COM_PowerSpect_CMB-TE-binned_R3.02.txt`.
Columns: ℓ_eff, D_ℓ (μK²), ±δD_ℓ, Planck best-fit. Reference: Planck 2018 results VI.

## Numbers

- Synthetic injected (H₀, ωc, Aₛ) = (69.0, 0.118, 2.05) → recovered within tolerance.
- Real Planck TT+TE: H₀ = 67.0, ωc = 0.1207, Aₛ = 2.104; χ² = 159.6 / 146 dof (χ²/dof = 1.09).
- Planck 2018: H₀ = 67.36, ωc = 0.1200, Aₛ = 2.10. **Contrast demo 05 local H₀ = 74.8.**
