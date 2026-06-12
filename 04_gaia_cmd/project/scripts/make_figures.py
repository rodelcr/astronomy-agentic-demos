"""Render the inspection figures for the Gaia CMD demo.

    python scripts/make_figures.py     # writes results/cmd.png, results/parallax_hist.png

The color-magnitude diagram is the inspection that matters: a real cluster traces a
tight main sequence. Scatter or a second sequence means contaminating field stars
(bad membership cuts). The parallax histogram shows the cluster as a sharp peak.
"""
from __future__ import annotations

import sys
from pathlib import Path
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cluster import cluster_distance, absolute_magnitude  # noqa: E402

LIT_DIST = 136.2   # pc, Pleiades (Gaia)


def main():
    rows = list(csv.DictReader(open(PROJECT / "data" / "real" / "pleiades_gaia.csv")))
    plx = np.array([float(r["parallax"]) for r in rows])
    err = np.array([float(r["parallax_error"]) for r in rows])
    g = np.array([float(r["phot_g_mean_mag"]) for r in rows])
    bp_rp = np.array([float(r["bp_rp"]) for r in rows])

    d = cluster_distance(plx, err)
    M_G = absolute_magnitude(g, plx)

    # --- CMD ---
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.plot(bp_rp, M_G, ".", ms=3, color="0.3")
    ax.invert_yaxis()
    ax.set_xlabel("BP − RP  (color)"); ax.set_ylabel("absolute G magnitude")
    ax.set_title(f"Pleiades CMD ({len(rows)} members)\nd = {d:.1f} pc  (literature {LIT_DIST})")
    fig.savefig(PROJECT / "results" / "cmd.png", dpi=130, bbox_inches="tight")

    # --- parallax histogram ---
    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    ax2.hist(plx, bins=40, color="0.5")
    ax2.axvline(1000.0 / d, color="crimson", lw=2, label=f"mean ϖ → {d:.1f} pc")
    ax2.set_xlabel("parallax (mas)"); ax2.set_ylabel("count")
    ax2.set_title("cluster members cluster in parallax too"); ax2.legend()
    fig2.savefig(PROJECT / "results" / "parallax_hist.png", dpi=130, bbox_inches="tight")
    print(f"distance = {d:.1f} pc; figures written")


if __name__ == "__main__":
    main()
