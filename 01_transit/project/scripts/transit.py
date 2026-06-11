"""transit.py — measure a planet's radius ratio Rp/R* from a transit light curve.

Importable AND runnable from the shell:

    from scripts.transit import fit_transit, phase_fold     # in a notebook/test
    python scripts/transit.py --data data/real/kepler8_q3.csv --period 3.52254 --t0 120.0

The estimator phase-folds the light curve at the known period and fits a trapezoid
(flat bottom + linear ingress/egress) to the folded transit. The fitted depth δ
gives the radius ratio for a uniform source: Rp/R* = √δ.
"""
from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import curve_fit


def rp_over_rstar(depth: float) -> float:
    """Radius ratio from fractional transit depth, uniform source: Rp/R* = √δ."""
    return float(np.sqrt(depth))


def phase_fold(time, period, t0):
    """Fold times onto phase in [-0.5, 0.5), zero at the transit center t0."""
    return ((np.asarray(time, float) - t0) / period + 0.5) % 1.0 - 0.5


def _trapezoid(phase, depth, half_total, half_flat, center):
    """Trapezoidal transit in *phase* units. Baseline 1, dip `depth`."""
    x = np.abs(phase - center)
    ramp = np.clip((half_total - x) / (half_total - half_flat), 0.0, 1.0)
    return 1.0 - depth * ramp


def fit_transit(time, flux, flux_err, period, t0, window=0.06):
    """Phase-fold and fit a trapezoid near the transit; return fit parameters.

    Parameters
    ----------
    time, flux, flux_err : array_like
        Light curve (flux normalized to ~1 out of transit).
    period, t0 : float
        Known orbital period and a transit-center epoch (same units as `time`).
    window : float
        Half-width in phase to keep around the transit for the fit. Restricting to
        the transit neighborhood keeps the trapezoid valid against stellar trends.

    Returns
    -------
    dict with keys: depth, rp_over_rstar, half_total, half_flat, center, and the
    fitted phase/flux arrays for plotting.
    """
    time = np.asarray(time, float)
    flux = np.asarray(flux, float)
    flux_err = np.asarray(flux_err, float)

    phase = phase_fold(time, period, t0)
    m = np.abs(phase) < window
    ph, fl, er = phase[m], flux[m], flux_err[m]
    order = np.argsort(ph)
    ph, fl, er = ph[order], fl[order], er[order]

    # initial guesses: depth from the dimmest 20%, durations a fraction of window
    depth0 = max(1.0 - np.percentile(fl, 10), 1e-4)
    p0 = [depth0, window * 0.5, window * 0.3, 0.0]
    bounds = ([0.0, 0.0, 0.0, -window], [1.0, window, window, window])
    popt, _ = curve_fit(_trapezoid, ph, fl, p0=p0, sigma=er,
                        absolute_sigma=True, bounds=bounds, maxfev=20000)
    depth, half_total, half_flat, center = popt
    if half_flat > half_total:                      # keep flat ⊂ total
        half_total, half_flat = half_flat, half_total
    return dict(
        depth=float(depth),
        rp_over_rstar=rp_over_rstar(depth),
        half_total=float(half_total),
        half_flat=float(half_flat),
        center=float(center),
        phase=ph,
        flux=fl,
        model=_trapezoid(ph, *popt),
    )


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", required=True, help="CSV with columns time,flux,flux_err")
    p.add_argument("--period", type=float, required=True, help="orbital period [days]")
    p.add_argument("--t0", type=float, required=True, help="transit-center epoch [days]")
    p.add_argument("--window", type=float, default=0.06, help="fit half-window in phase")
    args = p.parse_args()

    arr = np.loadtxt(args.data, delimiter=",", skiprows=1)
    res = fit_transit(arr[:, 0], arr[:, 1], arr[:, 2],
                      period=args.period, t0=args.t0, window=args.window)
    print(f"depth      = {res['depth']:.5f}")
    print(f"Rp/R*      = {res['rp_over_rstar']:.4f}")


if __name__ == "__main__":
    _main()
