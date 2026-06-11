"""Generate a synthetic transit light curve with a KNOWN depth.

The point of synthetic data is a ground-truth oracle: we build the light curve
from parameters we choose, write those parameters to params.json, and then the
test passes only if our estimator recovers them. Everything is seeded, so the
file is reproducible bit-for-bit.

    python make_synthetic.py        # writes lightcurve.csv + params.json here

The injected shape is a trapezoid (flat bottom + linear ingress/egress) — the same
model family our estimator fits, so this isolates the *fitting + noise handling*,
independent of the separate `batman` physical-model check.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# --- ground truth (the answer key) ---------------------------------------
TRUTH = dict(
    period=2.2,          # days
    t0=0.5,              # time of first transit center (days)
    depth=0.0100,        # fractional dip  -> rp_over_rstar = sqrt(depth) = 0.10
    rp_over_rstar=0.10,
    dur_total=0.120,     # T14, first-to-fourth contact (days)
    dur_flat=0.090,      # T23, second-to-third contact (days)
    noise=0.0020,        # per-point Gaussian sigma
    cadence=0.0204,      # ~30 min, like Kepler long cadence (days)
    span=27.0,           # total baseline (days)
    seed=42,
)


def trapezoid(time, period, t0, depth, dur_total, dur_flat):
    """Normalized flux for a trapezoidal transit, repeated every `period`."""
    half_t, half_f = dur_total / 2.0, dur_flat / 2.0
    phase = (time - t0 + 0.5 * period) % period - 0.5 * period  # nearest transit
    x = np.abs(phase)
    ramp = np.clip((half_t - x) / (half_t - half_f), 0.0, 1.0)   # 1 inside flat, 0 outside
    return 1.0 - depth * ramp


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    time = np.arange(0.0, t["span"], t["cadence"])
    flux = trapezoid(time, t["period"], t["t0"], t["depth"], t["dur_total"], t["dur_flat"])
    flux = flux + rng.normal(0.0, t["noise"], size=time.size)
    flux_err = np.full_like(time, t["noise"])

    out = np.column_stack([time, flux, flux_err])
    np.savetxt(HERE / "lightcurve.csv", out, delimiter=",",
               header="time,flux,flux_err", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {time.size} points; injected depth={t['depth']} "
          f"(Rp/R*={t['rp_over_rstar']})")


if __name__ == "__main__":
    main()
