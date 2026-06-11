"""Render the inspection figures for the period demo.

    python scripts/make_figures.py     # writes results/periodogram.png, results/folded.png

The periodogram shows the string-length minimum (our method) next to the
Lomb-Scargle maximum (the reference) — they should land on the same period. The
folded curve is the proof: at the right period the scattered points collapse onto
one clean pulsation cycle.
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
from scripts.variable import string_length_period, lombscargle_period, phase_fold  # noqa: E402

LIT_PERIOD = 4.9254   # V1154 Cyg, classical Cepheid


def main():
    arr = np.loadtxt(PROJECT / "data" / "real" / "v1154cyg_q3.csv",
                     delimiter=",", skiprows=1)
    t, m, me = arr[:, 0], arr[:, 1], arr[:, 2]

    P_sl, periods, lengths = string_length_period(t, m, 3.0, 7.0, n_periods=8000)
    P_ls = lombscargle_period(t, m, me, 3.0, 7.0)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(periods, lengths, "-", color="0.4", lw=1)
    ax.axvline(P_sl, color="crimson", lw=2, label=f"string-length min = {P_sl:.4f} d")
    ax.axvline(P_ls, color="steelblue", ls="--", lw=2, label=f"Lomb-Scargle = {P_ls:.4f} d")
    ax.set_xlabel("trial period (days)"); ax.set_ylabel("string length")
    ax.set_title("two independent period finders agree")
    ax.legend(fontsize=8)
    fig.savefig(PROJECT / "results" / "periodogram.png", dpi=130, bbox_inches="tight")

    ph = phase_fold(t, P_sl)
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(np.concatenate([ph, ph + 1]), np.concatenate([m, m]),
             ".", ms=3, color="0.4")           # two cycles for readability
    ax2.invert_yaxis()                          # brighter = up
    ax2.set_xlabel("phase"); ax2.set_ylabel("relative magnitude")
    ax2.set_title(f"V1154 Cyg folded at P = {P_sl:.4f} d  (literature {LIT_PERIOD})")
    fig2.savefig(PROJECT / "results" / "folded.png", dpi=130, bbox_inches="tight")
    print(f"string-length P={P_sl:.4f} d, Lomb-Scargle P={P_ls:.4f} d; figures written")


if __name__ == "__main__":
    main()
