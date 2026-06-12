# NOTES — Hubble demo

## Decisions

- **Through-origin fit.** Physics fixes the intercept at zero (no distance, no
  cosmological recession). A free intercept would absorb signal and bias the slope; we
  report the through-origin slope and mention the intercept-fit only as a diagnostic.
- **Bootstrap for the error bar.** It's empirical, assumption-light, and *visible* (a
  histogram of refit slopes) — better pedagogy than a formula students can't see.
- **Distance & velocity cuts.** 10–200 Mpc and Vcmb > 500 km/s keep us in the clean
  Hubble flow; nearer galaxies are dominated by peculiar velocities.

## Honest caveat (don't oversell the error bar)

The bootstrap gives the *statistical* error (~1 km/s/Mpc here) — how much H₀ wobbles
under resampling. It says **nothing** about the dominant real-world uncertainty:
systematic errors in the distance scale (the "rungs" of the distance ladder). The
Hubble tension (local ~73 vs Planck 67.4) is a *systematics* disagreement, not one the
bootstrap could reveal. The notebook states this explicitly.

## Data source (reproducible)

VizieR catalog `J/AJ/152/50` (Cosmicflows-3, Tully+ 2016), via
`astroquery.vizier`, columns `<Dist>` (Mpc) and `<Vcmb>` (km/s), filtered
`Dist 10..200`, `Vcmb > 500`, random 600-galaxy subsample (seed 0).

## Numbers

- Synthetic injected H₀ = 70 → recovered within 5%; bootstrap interval brackets 70.
- Real Cosmicflows-3: H₀ = 74.8 (+0.8/−0.8) km/s/Mpc; closed form matches scipy to 1e-6.
