"""cluster.py — distance to a star cluster from Gaia parallaxes, and its CMD.

Importable AND runnable from the shell:

    from scripts.cluster import cluster_distance, absolute_magnitude
    python scripts/cluster.py --data data/real/pleiades_gaia.csv

The cluster distance comes from the members' parallaxes. The subtlety the demo
teaches: averaging 1/parallax star-by-star is *biased* when parallaxes are noisy
(the 1/ϖ transform is nonlinear). The robust estimate averages the parallaxes first
(inverse-variance weighted) and inverts once. We validate the conversion against
`astropy.coordinates.Distance`.
"""
from __future__ import annotations

import argparse

import numpy as np


def parallax_to_distance(parallax_mas):
    """Distance in parsecs from parallax in milliarcsec: d = 1000 / ϖ."""
    return 1000.0 / np.asarray(parallax_mas, float)


def cluster_distance(parallax_mas, parallax_error_mas):
    """Cluster distance [pc] from the inverse-variance-weighted mean parallax.

    Averaging parallax (a linear quantity) then inverting avoids the bias of
    averaging 1/ϖ when the parallaxes are noisy.
    """
    p = np.asarray(parallax_mas, float)
    e = np.asarray(parallax_error_mas, float)
    w = 1.0 / e ** 2
    p_mean = np.sum(w * p) / np.sum(w)
    return float(1000.0 / p_mean)


def absolute_magnitude(app_mag, parallax_mas):
    """Absolute magnitude from apparent mag and parallax: M = m + 5 + 5 log₁₀(ϖ/1000)."""
    p = np.asarray(parallax_mas, float)
    return np.asarray(app_mag, float) + 5.0 + 5.0 * np.log10(p / 1000.0)


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", required=True, help="Gaia CSV (parallax, parallax_error, ...)")
    args = p.parse_args()
    import csv
    rows = list(csv.DictReader(open(args.data)))
    plx = np.array([float(r["parallax"]) for r in rows])
    err = np.array([float(r["parallax_error"]) for r in rows])
    d = cluster_distance(plx, err)
    print(f"n members      = {len(rows)}")
    print(f"median parallax= {np.median(plx):.3f} mas")
    print(f"distance       = {d:.1f} pc")


if __name__ == "__main__":
    _main()
