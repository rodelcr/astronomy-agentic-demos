"""make_figures.py — the two committed figures.

    python scripts/make_figures.py        # writes results/orrery.png + results/kepler_third_law.png

1. orrery.png            — a top-down (J2000 ecliptic) snapshot: the Sun, each planet, and its
   orbit trace. *Look*: the orbits should be near-concentric, ordered, and closed. A tilted or
   broken set of orbits is the ICRF→ecliptic frame bug.
2. kepler_third_law.png  — P² (yr²) vs a³ (AU³) for the 8 planets, recovered from the ephemeris.
   Kepler's third law makes this the identity line P² = a³.
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
from scripts.ephemeris import (  # noqa: E402
    heliocentric_ecliptic, orbit_track, orbital_period, semi_major_axis, PLANETS, _load,
)

RESULTS = PROJECT / "results"
COLORS = {"mercury": "#8c8c8c", "venus": "#d9a066", "earth": "#3b7dd8", "mars": "#c1440e",
          "jupiter": "#d8a25e", "saturn": "#e3c777", "uranus": "#8fd6e1", "neptune": "#4b6fd6"}


def orrery(date=(2026, 6, 12)):
    ts, _ = _load()
    t = ts.utc(*date)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    views = [(PLANETS[:4], 1.8, "inner solar system"), (PLANETS, 31.0, "all eight planets")]
    for ax, (bodies, lim, title) in zip(axes, views):
        ax.plot(0, 0, "o", color="gold", ms=14, zorder=5)
        for b in bodies:
            xyz = orbit_track(b, 500)
            ax.plot(xyz[0], xyz[1], "-", lw=0.8, color=COLORS[b], alpha=0.55)
            x, y, _ = heliocentric_ecliptic(b, t)
            ax.plot(x, y, "o", color=COLORS[b], ms=7, zorder=4)
            ax.annotate(b, (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
        ax.set_aspect("equal")
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        ax.set_xlabel("x (AU)"); ax.set_ylabel("y (AU)")
        ax.set_title(title)
    fig.suptitle(f"Orrery — heliocentric J2000 ecliptic, {date[0]:04d}-{date[1]:02d}-{date[2]:02d}")
    fig.tight_layout()
    fig.savefig(RESULTS / "orrery.png", dpi=130)
    plt.close(fig)
    print("wrote results/orrery.png")


def kepler():
    a = np.array([semi_major_axis(b) for b in PLANETS])
    P = np.array([orbital_period(b) for b in PLANETS]) / 365.25
    fig, ax = plt.subplots(figsize=(6.2, 6))
    xx = np.logspace(-2, 4.6, 50)
    ax.plot(xx, xx, "-", color="0.55", lw=1.5, label="P² = a³  (Kepler III)")
    ax.scatter(a ** 3, P ** 2, s=45, color="crimson", zorder=3, label="planets (from de440s)")
    for b, ai, Pi in zip(PLANETS, a, P):
        ax.annotate(b, (ai ** 3, Pi ** 2), textcoords="offset points", xytext=(6, -2), fontsize=8)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("a³  (AU³)"); ax.set_ylabel("P²  (yr²)")
    ax.set_title("Kepler's third law, recovered from the ephemeris")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(RESULTS / "kepler_third_law.png", dpi=130)
    plt.close(fig)
    print("wrote results/kepler_third_law.png")


if __name__ == "__main__":
    RESULTS.mkdir(exist_ok=True)
    orrery()
    kepler()
