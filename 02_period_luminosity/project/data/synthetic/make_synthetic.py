"""Generate a synthetic variable-star light curve with a KNOWN period.

Cepheid light curves are periodic but asymmetric (fast rise, slow decline), so we
build the signal from a few Fourier harmonics. Sampling is deliberately uneven
(random gaps) — like real ground-based data — which is exactly the regime where
period-finding is non-trivial. Everything is seeded.

    python make_synthetic.py     # writes lightcurve.csv + params.json here
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

TRUTH = dict(
    period=3.7,                  # days  (the answer key)
    amplitude=0.40,              # mag, peak-to-peak-ish
    n_points=300,
    noise=0.02,                  # mag
    span=60.0,                   # days
    seed=7,
    # Fourier coefficients (relative) giving an asymmetric Cepheid-like shape
    harmonics=[1.0, 0.4, 0.15],
    phases=[0.0, 0.6, 1.1],
)


def cepheid_shape(phase, harmonics, phases):
    """Asymmetric periodic light curve from a small Fourier series (mag units)."""
    y = np.zeros_like(phase)
    for k, (a, p) in enumerate(zip(harmonics, phases), start=1):
        y += a * np.sin(2 * np.pi * k * phase + p)
    return y


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    # uneven sampling: random times across the baseline, sorted
    time = np.sort(rng.uniform(0, t["span"], t["n_points"]))
    phase = (time / t["period"]) % 1.0
    shape = cepheid_shape(phase, t["harmonics"], t["phases"])
    shape *= t["amplitude"] / np.ptp(shape)          # scale to requested amplitude
    mag = 12.0 + shape + rng.normal(0, t["noise"], time.size)
    mag_err = np.full_like(time, t["noise"])

    out = np.column_stack([time, mag, mag_err])
    np.savetxt(HERE / "lightcurve.csv", out, delimiter=",",
               header="time,mag,mag_err", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {time.size} points; injected period={t['period']} d")


if __name__ == "__main__":
    main()
