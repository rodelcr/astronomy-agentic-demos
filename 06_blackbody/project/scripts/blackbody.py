"""blackbody.py — fit a Planck blackbody to a spectrum and recover its temperature.

Importable AND runnable from the shell:

    from scripts.blackbody import planck_MJy, fit_temperature
    python scripts/blackbody.py --data data/real/firas_cmb.csv

A blackbody's spectrum depends on a single number — its temperature. The Planck law
fixes the shape *and* the absolute brightness, so fitting it to a calibrated spectrum
(no free scale) returns the temperature directly. We validate our Planck function
against `astropy.modeling.BlackBody`.
"""
from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import curve_fit

# physical constants (CGS-ish, chosen so the output is MJy/sr)
_H = 6.62607015e-27      # erg s
_K = 1.380649e-16        # erg / K
_C = 2.99792458e10       # cm / s


def planck_MJy(freq_icm, T):
    """Planck spectral radiance B_ν(T) in MJy/sr, for frequency in cm⁻¹.

    B_ν = 2hν³/c² · 1/(exp(hν/kT) − 1); converted to MJy/sr (1 MJy = 1e-17 erg/s/cm²/Hz).
    """
    nu = np.asarray(freq_icm, float) * _C          # cm⁻¹ → Hz
    B_cgs = (2 * _H * nu ** 3 / _C ** 2) / (np.expm1(_H * nu / (_K * T)))  # erg/s/cm²/Hz/sr
    return B_cgs / 1e-17                            # → MJy/sr


def fit_temperature(freq_icm, intensity_MJy, uncertainty_MJy=None, T0=3.0):
    """Fit the Planck law to a calibrated spectrum; return (T, T_err) in kelvin."""
    popt, pcov = curve_fit(planck_MJy, np.asarray(freq_icm, float),
                           np.asarray(intensity_MJy, float),
                           p0=[T0], sigma=uncertainty_MJy, absolute_sigma=uncertainty_MJy is not None)
    return float(popt[0]), float(np.sqrt(pcov[0, 0]))


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", required=True, help="CSV: freq_icm,intensity_MJy_sr,uncertainty_MJy_sr")
    args = p.parse_args()
    arr = np.loadtxt(args.data, delimiter=",", skiprows=1)
    unc = arr[:, 2] if arr.shape[1] > 2 else None
    T, T_err = fit_temperature(arr[:, 0], arr[:, 1], unc)
    print(f"T = {T:.4f} ± {T_err:.4f} K")


if __name__ == "__main__":
    _main()
