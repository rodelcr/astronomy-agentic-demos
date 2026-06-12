"""Render the inspection figures for the blackbody demo.

    python scripts/make_figures.py     # writes results/firas_fit.png, results/residuals.png

The FIRAS spectrum is the most famous plot in cosmology: the data points sit exactly
on the Planck curve, with error bars far smaller than the marker. The residual panel
makes the point quantitatively — the CMB is a blackbody to a fraction of a percent.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.blackbody import planck_MJy, fit_temperature  # noqa: E402


def main():
    arr = np.loadtxt(PROJECT / "data" / "real" / "firas_cmb.csv", delimiter=",", skiprows=1)
    freq, intensity, unc = arr[:, 0], arr[:, 1], arr[:, 2]
    T, T_err = fit_temperature(freq, intensity, unc)

    grid = np.linspace(freq.min(), freq.max(), 300)
    model = planck_MJy(grid, T)
    resid = intensity - planck_MJy(freq, T)

    fig = plt.figure(figsize=(7, 6))
    gs = GridSpec(2, 1, height_ratios=[3, 1], hspace=0.06)
    ax = fig.add_subplot(gs[0])
    ax.plot(grid, model, "-", color="crimson", lw=2, label=f"Planck fit, T = {T:.4f} K")
    # error bars are ~400× smaller than the points — scale up ×400 so they're visible
    ax.errorbar(freq, intensity, yerr=unc * 400, fmt="o", color="0.2", ms=4,
                label="FIRAS (error ×400)")
    ax.set_ylabel("intensity (MJy/sr)")
    ax.set_title("The CMB is a blackbody — COBE/FIRAS")
    ax.legend()
    axr = fig.add_subplot(gs[1], sharex=ax)
    axr.axhline(0, color="crimson", lw=1)
    axr.errorbar(freq, resid * 1000, yerr=unc * 1000, fmt="o", color="0.2", ms=3)
    axr.set_ylabel("resid\n(kJy/sr)"); axr.set_xlabel("frequency (cm⁻¹)")
    fig.savefig(PROJECT / "results" / "firas_fit.png", dpi=130, bbox_inches="tight")

    fig2, ax2 = plt.subplots(figsize=(6, 3.2))
    ax2.errorbar(freq, resid * 1000, yerr=unc * 1000, fmt="o", color="0.3", ms=3)
    ax2.axhline(0, color="crimson")
    ax2.set_xlabel("frequency (cm⁻¹)"); ax2.set_ylabel("residual (kJy/sr)")
    ax2.set_title("residuals: a perfect blackbody to < 0.01%")
    fig2.savefig(PROJECT / "results" / "residuals.png", dpi=130, bbox_inches="tight")
    print(f"T = {T:.4f} ± {T_err:.4f} K; figures written")


if __name__ == "__main__":
    main()
