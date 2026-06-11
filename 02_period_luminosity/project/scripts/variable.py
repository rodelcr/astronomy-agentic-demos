"""variable.py — find the pulsation period of a variable star.

Importable AND runnable from the shell:

    from scripts.variable import string_length_period, phase_fold
    python scripts/variable.py --data data/real/v1154cyg_q3.csv --pmin 1 --pmax 10

The period is found with the **string-length** method (Dworetsky 1983), which is
architecturally independent of Fourier/Lomb-Scargle: for each trial period we fold,
sort by phase, and sum the length of the line joining consecutive (phase, mag)
points. The true period stacks the points into a tight curve → shortest string.
Validating *this* against `astropy`'s Lomb-Scargle is a real cross-check: two
unrelated methods must agree.
"""
from __future__ import annotations

import argparse

import numpy as np


def phase_fold(time, period, t0=0.0):
    """Fold times onto phase in [0, 1)."""
    return ((np.asarray(time, float) - t0) / period) % 1.0


def _string_length(phase, mag):
    """Total length of the string joining points sorted by phase (wrapping)."""
    order = np.argsort(phase)
    ph, m = phase[order], mag[order]
    dph = np.diff(ph, append=ph[0] + 1.0)          # wrap last->first
    dm = np.diff(m, append=m[0])
    # normalize mag scale so phase and mag contribute comparably
    span = np.ptp(m) or 1.0
    return float(np.sum(np.hypot(dph, dm / span)))


def string_length_period(time, mag, pmin, pmax, n_periods=20000):
    """Best period in [pmin, pmax] by minimizing string length over trial periods."""
    time = np.asarray(time, float)
    mag = np.asarray(mag, float)
    periods = np.linspace(pmin, pmax, n_periods)
    lengths = np.array([_string_length(phase_fold(time, P), mag) for P in periods])
    return float(periods[np.argmin(lengths)]), periods, lengths


def lombscargle_period(time, mag, mag_err, pmin, pmax):
    """Reference period from astropy Lomb-Scargle (the external answer key)."""
    from astropy.timeseries import LombScargle
    freq, power = LombScargle(time, mag, mag_err).autopower(
        minimum_frequency=1.0 / pmax, maximum_frequency=1.0 / pmin)
    return float(1.0 / freq[np.argmax(power)])


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", required=True, help="CSV with columns time,mag,mag_err")
    p.add_argument("--pmin", type=float, default=1.0, help="min trial period [days]")
    p.add_argument("--pmax", type=float, default=10.0, help="max trial period [days]")
    args = p.parse_args()
    arr = np.loadtxt(args.data, delimiter=",", skiprows=1)
    P_sl, _, _ = string_length_period(arr[:, 0], arr[:, 1], args.pmin, args.pmax)
    print(f"string-length period = {P_sl:.4f} d")


if __name__ == "__main__":
    _main()
