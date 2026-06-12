"""Render the inspection figures for the Hubble demo.

    python scripts/make_figures.py     # writes results/hubble_diagram.png, results/bootstrap.png

The Hubble diagram is the inspection: real galaxies scatter around the v = H₀d line
because of peculiar velocities, but the linear trend should be unmistakable and pass
through the origin. The bootstrap histogram is the error bar made visible.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.hubble import fit_h0, bootstrap_h0  # noqa: E402


def main():
    arr = np.loadtxt(PROJECT / "data" / "real" / "cosmicflows3.csv",
                     delimiter=",", skiprows=1)
    dist, vel = arr[:, 0], arr[:, 1]
    H0 = fit_h0(dist, vel)
    med, lo, hi = bootstrap_h0(dist, vel, n_boot=3000)
    boots = _boot_samples(dist, vel)

    # --- Hubble diagram ---
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(dist, vel, ".", ms=4, color="0.4", alpha=0.6, label="Cosmicflows-3 galaxies")
    xx = np.array([0, dist.max()])
    ax.plot(xx, H0 * xx, "-", color="crimson", lw=2,
            label=f"v = H₀ d,  H₀ = {H0:.1f} km/s/Mpc")
    ax.set_xlabel("distance (Mpc)"); ax.set_ylabel("recession velocity (km/s)")
    ax.set_title("Hubble diagram"); ax.legend(loc="upper left", fontsize=9)
    fig.savefig(PROJECT / "results" / "hubble_diagram.png", dpi=130, bbox_inches="tight")

    # --- bootstrap distribution ---
    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    ax2.hist(boots, bins=40, color="0.5")
    ax2.axvline(med, color="crimson", lw=2, label=f"H₀ = {med:.1f} (+{hi-med:.1f}/-{med-lo:.1f})")
    ax2.axvspan(lo, hi, color="crimson", alpha=0.15)
    ax2.set_xlabel("bootstrap H₀ (km/s/Mpc)"); ax2.set_ylabel("count")
    ax2.set_title("bootstrap error bar"); ax2.legend()
    fig2.savefig(PROJECT / "results" / "bootstrap.png", dpi=130, bbox_inches="tight")
    print(f"H0 = {H0:.1f} (+{hi-med:.1f}/-{med-lo:.1f}) km/s/Mpc; figures written")


def _boot_samples(dist, vel, n_boot=3000, seed=0):
    rng = np.random.default_rng(seed)
    n = dist.size
    return np.array([fit_h0(dist[i], vel[i])
                     for i in (rng.integers(0, n, n) for _ in range(n_boot))])


if __name__ == "__main__":
    main()
