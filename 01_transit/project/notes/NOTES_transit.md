# NOTES — transit demo

In-progress thinking, dead ends, and decisions. (The clean summary is in
`HANDOFF_transit.md`.)

## Decisions

- **Trapezoid, not full Mandel–Agol.** An undergrad's first fit should expose one
  idea — depth → radius — not limb-darkening degeneracies. We *validate* against the
  full physical model via `batman` instead of fitting it ourselves.
- **Fit only |phase| < 0.06.** Restricting to the transit neighborhood keeps the
  flat-baseline assumption valid against slow stellar variability and removes the
  need to detrend the whole quarter.
- **t0 from Box-Least-Squares.** We don't fit the period (single quarter, multimodal).
  Period is the literature value (3.52254 d); the epoch comes from `BoxLeastSquares`
  evaluated at that period → t0 = 170.4408 BKJD.

## Dead end (worth remembering)

First version of `phase_fold` was `((t - t0)/P) % 1 - 0.5`. That puts the transit
center at phase **−0.5** (the panel edge), not 0, so the |phase|<0.06 window caught
only out-of-transit baseline and the fit returned depth ≈ 6e-5 — a "planet" 40×
too small. Both tests failed. Fix: add the half-period offset *before* the modulo,
`((t - t0)/P + 0.5) % 1 - 0.5`, centering the transit at 0. The failing **batman**
test is what caught it — a synthetic-only suite would have hidden the bug behind a
loose tolerance.

## Numbers

- Synthetic injected depth 0.0100 (Rp/R* = 0.100) → recovered within 5%.
- batman uniform-source rp = 0.100 → recovered within 3%.
- Real Kepler-8 b: Rp/R* = 0.0935 vs literature 0.0944 (~1% low; consistent with
  the trapezoid underfitting the limb-darkened, rounded transit bottom).
