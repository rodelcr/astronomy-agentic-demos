# NOTES — CMB map → power spectrum demo

## Decisions

- **Compute the spectrum from a map, not from pre-binned files.** The whole lesson is the
  spherical-harmonic decomposition; the binned Planck spectra hide it. (This demo was rebuilt
  from a binned-spectra version after the user corrected that — see TRANSCRIPT.)
- **Hand-rolled `cl_from_alm`.** We implement Ĉ_ℓ = 1/(2ℓ+1)Σ_m|a_ℓm|² explicitly so the
  estimator is visible, and validate it against `healpy.alm2cl` (machine precision).
- **healpy for the SHT integral, NaMaster for masking.** Evaluating a_ℓm at Nside 2048 and the
  spin-2 (polarization) transforms are healpy's job; the rigorous masked mode-coupling is
  NaMaster's. We don't reimplement either — we *use them as answer keys*.
- **Synthetic map regenerated from seed.** 50M pixels (~400 MB) is too big to commit; the
  committed data product is the bandpowers CSV. The real map is shipped only downgraded (Nside
  256, ~3 MB).

## Intermediate problems this rebuild surfaced (the agentic-coding lesson)

A catalog of the messy steps between "fit the CMB" and the answer — each solved en route. The
narrative version is in `walkthrough/TRANSCRIPT.md`.

| # | Problem | Resolution |
|---|---------|-----------|
| 0 | First build used pre-binned spectra (skipped the computation) | full rebuild around map → aₗₘ → Cₗ; binned CSVs deleted |
| 1 | Is the by-hand m-sum correct? | validated `cl_from_alm` vs `healpy.alm2cl` → 7×10⁻¹⁵ |
| 2 | 2 GB SMICA download kept truncating (598 MB / 1.2 GB / …) | `curl -C - --max-time` resume loop in the background; built the offline core meanwhile |
| 3 | `NmtBin.from_nside_linear(..., lmax=)` → TypeError | read the traceback; dropped the kwarg (pymaster 2.7 API) |
| 4 | Recovery looked 5% biased | a **comparison** artifact (bin-average vs bin-centre); bin the input the same way |
| 5 | A real +2.2% bias; fit gave H₀ = 65.4 not 69 | map lacked the **pixel window**; apply it at generation so pixwin² correction is exact → H₀ = 69.19 |

The distinction between #4 (don't touch the code) and #5 (fix the physics) is the crux: both
showed up as "the spectrum is biased," and only a diagnostic — the ratio of map-derived to
input, *mean and scatter vs the predicted cosmic-variance error* — told them apart.

## Data source (reproducible)

Real map: Planck SMICA `COM_CMB_IQU-smica_2048_R3.00_full.fits` from the ESA Planck Legacy
Archive (`scripts/fetch_real_map.py`), temperature (I_STOKES, K→μK) + confidence mask (TMASK),
`ud_grade`'d to Nside 256.

## Numbers

- `cl_from_alm` vs `healpy.alm2cl`: 7×10⁻¹⁵ (machine precision).
- Synthetic recovery (Nside 1024): binned map-derived ≈ input to a few percent.
- NaMaster vs naive fsky on a masked sky: agree to ~10% (residual = mode-coupling).
- Map-derived bandpowers fit: H₀ = 69.19 (injected 69.0), ωc = 0.1169 (0.118), Aₛ = 2.049 (2.05),
  χ²/dof ≈ 1.8 (single realization, cosmic-variance errors).
- Real SMICA (Nside 256): first acoustic peak recovered, tracking Planck ΛCDM to ℓ ≈ 500.
