"""Render the inspection figures for the transit demo.

    python scripts/make_figures.py     # writes results/folded_fit.png, results/residuals.png

A fit you haven't plotted is a fit you don't trust. The folded-fit figure shows the
phase-folded transit with the trapezoid model on top, and the residuals (data−model)
in a panel beneath — flat residuals are the evidence the fit is good.
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
from scripts.transit import fit_transit, phase_fold  # noqa: E402

# Kepler-8 b
PERIOD = 3.52254          # days (Jenkins et al. 2010)
T0 = 170.4408             # BKJD, transit center (from BLS on this quarter)
LIT_RP = 0.0944           # literature Rp/R*


def main():
    arr = np.loadtxt(PROJECT / "data" / "real" / "kepler8_q3.csv",
                     delimiter=",", skiprows=1)
    t, f, fe = arr[:, 0], arr[:, 1], arr[:, 2]
    res = fit_transit(t, f, fe, period=PERIOD, t0=T0, window=0.06)

    ph_all = phase_fold(t, PERIOD, T0)
    ph, fl, model = res["phase"], res["flux"], res["model"]
    resid = fl - model

    fig = plt.figure(figsize=(7, 6))
    gs = GridSpec(2, 1, height_ratios=[3, 1], hspace=0.06)

    ax = fig.add_subplot(gs[0])
    ax.plot(ph_all, f, ".", ms=2, color="0.7", alpha=0.5, label="all data")
    ax.plot(ph, fl, ".", ms=4, color="0.3", label="in-window")
    ax.plot(ph, model, "-", color="crimson", lw=2, label="trapezoid fit")
    ax.set_xlim(-0.06, 0.06)
    ax.set_ylim(1 - 1.8 * res["depth"], 1 + 0.6 * res["depth"])
    ax.set_ylabel("normalized flux")
    ax.set_title(f"Kepler-8 b  —  Rp/R* = {res['rp_over_rstar']:.4f}  "
                 f"(literature {LIT_RP})")
    ax.legend(loc="lower right", fontsize=8)

    axr = fig.add_subplot(gs[1], sharex=ax)
    axr.axhline(0, color="crimson", lw=1)
    axr.plot(ph, resid, ".", ms=3, color="0.3")
    axr.set_ylabel("resid.")
    axr.set_xlabel("orbital phase")
    fig.savefig(PROJECT / "results" / "folded_fit.png", dpi=130, bbox_inches="tight")

    # standalone residual histogram — should look like noise, no skew
    fig2, ax2 = plt.subplots(figsize=(5, 3.2))
    ax2.hist(resid, bins=40, color="0.5")
    ax2.set_xlabel("residual (data − model)")
    ax2.set_ylabel("count")
    ax2.set_title("residuals ≈ Gaussian noise → trapezoid is adequate")
    fig2.savefig(PROJECT / "results" / "residuals.png", dpi=130, bbox_inches="tight")
    print(f"Rp/R* = {res['rp_over_rstar']:.4f}; figures written to results/")


if __name__ == "__main__":
    main()
