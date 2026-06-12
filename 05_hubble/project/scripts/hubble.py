"""hubble.py — Hubble's constant from galaxy distances and recession velocities.

Importable AND runnable from the shell:

    from scripts.hubble import fit_h0, bootstrap_h0
    python scripts/hubble.py --data data/real/cosmicflows3.csv

Hubble's law is v = H₀ d: recession velocity grows linearly with distance, and the
slope is H₀. We fit a line *through the origin* (a galaxy at zero distance has zero
cosmological velocity) by least squares — a one-line closed form — and put an error
bar on it by **bootstrap** (refit many resampled datasets). The closed form is
validated against `scipy`.
"""
from __future__ import annotations

import argparse

import numpy as np


def fit_h0(dist, vel):
    """Through-origin least-squares slope: H₀ = Σ(d·v) / Σ(d²)  [km/s/Mpc]."""
    d = np.asarray(dist, float)
    v = np.asarray(vel, float)
    return float(np.sum(d * v) / np.sum(d * d))


def bootstrap_h0(dist, vel, n_boot=2000, seed=0):
    """Bootstrap distribution of H₀: refit on n_boot resamples (with replacement).

    Returns (median, lo, hi) where lo/hi are the 16th/84th percentiles (≈1σ).
    """
    d = np.asarray(dist, float)
    v = np.asarray(vel, float)
    rng = np.random.default_rng(seed)
    n = d.size
    boots = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[i] = fit_h0(d[idx], v[idx])
    return float(np.median(boots)), float(np.percentile(boots, 16)), float(np.percentile(boots, 84))


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", required=True, help="CSV with columns dist_mpc,vel_kms")
    p.add_argument("--n-boot", type=int, default=2000, help="bootstrap resamples")
    args = p.parse_args()
    arr = np.loadtxt(args.data, delimiter=",", skiprows=1)
    H0 = fit_h0(arr[:, 0], arr[:, 1])
    med, lo, hi = bootstrap_h0(arr[:, 0], arr[:, 1], n_boot=args.n_boot)
    print(f"n galaxies = {len(arr)}")
    print(f"H0         = {H0:.1f}  (+{hi - med:.1f} / -{med - lo:.1f}) km/s/Mpc")


if __name__ == "__main__":
    _main()
