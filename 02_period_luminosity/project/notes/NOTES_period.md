# NOTES — period demo

## Decisions

- **String length, not our own Lomb-Scargle.** The external check is only meaningful
  if the two methods are independent. String-length (geometry of the folded curve)
  and Lomb-Scargle (Fourier power) share no machinery, so their agreement is real
  evidence — not a tautology.
- **SAP flux, not PDCSAP.** The PDC pipeline removes long-timescale trends and can
  suppress genuine stellar variability. For a ~5-day pulsation we keep SAP and accept
  small instrumental trends.
- **Magnitudes, not flux.** Pulsation amplitude is naturally expressed in mag; we use
  −2.5 log₁₀(flux / median).

## Dead end / gotcha

A naive string length adds `|Δphase|` and `|Δmag|` in raw units, but phase ∈ [0,1)
and magnitude spans ~0.3 — so magnitude dominates and the metric barely responds to
period. Fix: normalize the magnitude axis by its range before summing
(`np.hypot(dphase, dmag / span)`), so both axes contribute comparably. Without this
the minimum is shallow and the recovered period is noisy.

## Numbers

- Synthetic injected period 3.7 d → recovered within 1%.
- Real V1154 Cyg: string-length 4.9252 d, Lomb-Scargle 4.9124 d (agree 0.26%);
  literature 4.9254 d.
- Leavitt-law distance ~2.6 kpc (scaffolded; depends on adopted M_V calibration,
  V_app = 9.06, A_V ≈ 0.25). Literature distance ~3 kpc — same order, as expected for
  a single-calibration estimate.
