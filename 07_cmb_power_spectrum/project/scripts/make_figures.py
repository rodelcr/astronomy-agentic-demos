"""Render the inspection figures for the CMB demo.

    python scripts/make_figures.py     # fits real Planck data, writes results/

Produces the two iconic plots: the TT acoustic-peak spectrum and the TE
cross-spectrum, each with the best-fit ΛCDM theory over the Planck data and a residual
panel. The best-fit parameters are cached to results/best_fit.json (the fit takes ~20 s).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cmb import theory_spectrum, bin_to_data, fit_cosmology, load_planck  # noqa: E402

PLANCK = dict(H0=67.36, omch2=0.1200, As=2.100)


def _panel(fig, gs_row, ell, D_model, l, D, dD, ylabel, title):
    inner = gs_row.subgridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax = fig.add_subplot(inner[0])
    ax.plot(ell, D_model, "-", color="crimson", lw=1.5, label="best-fit ΛCDM (CAMB)")
    ax.errorbar(l, D, yerr=dD, fmt="o", ms=3, color="0.2", label="Planck 2018")
    ax.set_xlim(0, 2500); ax.set_ylabel(ylabel); ax.set_title(title); ax.legend(fontsize=8)
    axr = fig.add_subplot(inner[1], sharex=ax)
    axr.axhline(0, color="crimson", lw=1)
    axr.errorbar(l, D - bin_to_data(ell, D_model, l), yerr=dD, fmt="o", ms=3, color="0.2")
    axr.set_ylabel("resid"); axr.set_xlabel("multipole ℓ")
    return ax


def main():
    data = load_planck(PROJECT / "data" / "real" / "planck_tt_binned.csv",
                       PROJECT / "data" / "real" / "planck_te_binned.csv")
    fit = fit_cosmology(data)
    (PROJECT / "results" / "best_fit.json").write_text(json.dumps(fit, indent=2))
    ell, D_tt, D_te = theory_spectrum(fit["H0"], fit["omch2"], fit["As"])

    # --- TT ---
    fig = plt.figure(figsize=(7.5, 5))
    gs = GridSpec(1, 1)
    _panel(fig, gs[0], ell, D_tt, *data["tt"],
           r"$\mathcal{D}_\ell^{TT}\ (\mu K^2)$",
           f"CMB temperature spectrum — H₀={fit['H0']:.1f}, ωc={fit['omch2']:.4f}, "
           f"As={fit['As']:.3f}  (χ²/dof={fit['chi2']/fit['ndof']:.2f})")
    fig.savefig(PROJECT / "results" / "tt_fit.png", dpi=130, bbox_inches="tight")

    # --- TE ---
    fig2 = plt.figure(figsize=(7.5, 5))
    gs2 = GridSpec(1, 1)
    _panel(fig2, gs2[0], ell, D_te, *data["te"],
           r"$\mathcal{D}_\ell^{TE}\ (\mu K^2)$",
           "CMB temperature–polarization cross spectrum (TE)")
    fig2.savefig(PROJECT / "results" / "te_fit.png", dpi=130, bbox_inches="tight")

    print(f"H0={fit['H0']:.2f}, omch2={fit['omch2']:.4f}, As={fit['As']:.3f}; "
          f"chi2/dof={fit['chi2']/fit['ndof']:.2f}; figures + best_fit.json written")


if __name__ == "__main__":
    main()
