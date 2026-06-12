"""cosmofit.py — fit a ΛCDM cosmology to a MAP-DERIVED power spectrum.

The companion to powerspectrum.py: once you've extracted bandpowers from a sky map by
spherical-harmonic decomposition, you fit a cosmological model to them. The theory comes
from CAMB; we fit {H0, ωc, As} by minimizing a χ² with **cosmic-variance** errors (the
fundamental floor — you only have one sky, so each C_ℓ is measured from 2ℓ+1 modes).

    from scripts.cosmofit import theory_spectrum, fit_cosmology, cosmic_variance

`theory_spectrum` returns lensed D_ℓ = ℓ(ℓ+1)C_ℓ/2π in μK² (TT, TE), as before — the GUI
and earlier code use this signature.
"""
from __future__ import annotations

import numpy as np

FIXED = dict(ombh2=0.02237, ns=0.9649, tau=0.0544)
FIDUCIAL = dict(H0=67.36, omch2=0.1200, As=2.100)   # As in units of 1e-9


def theory_spectrum(H0, omch2, As, ombh2=FIXED["ombh2"], ns=FIXED["ns"],
                    tau=FIXED["tau"], lmax=2600):
    """Lensed D_ℓ = ℓ(ℓ+1)C_ℓ/2π in μK² for TT and TE, via CAMB. As in 1e-9."""
    import camb
    pars = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, ns=ns,
                           As=As * 1e-9, tau=tau, lmax=lmax)
    cl = camb.get_results(pars).get_cmb_power_spectra(
        pars, CMB_unit="muK", spectra=["total"])["total"]
    return np.arange(cl.shape[0]), cl[:, 0], cl[:, 3]


def theory_cl_tt(H0, omch2, As, lmax=2600, **kw):
    """Raw (un-ℓ-weighted) TT C_ℓ in μK² — to compare with map-derived C_ℓ."""
    import camb
    pars = camb.set_params(H0=H0, ombh2=kw.get("ombh2", FIXED["ombh2"]),
                           omch2=omch2, ns=kw.get("ns", FIXED["ns"]), As=As * 1e-9,
                           tau=kw.get("tau", FIXED["tau"]), lmax=lmax)
    cl = camb.get_results(pars).get_cmb_power_spectra(
        pars, CMB_unit="muK", raw_cl=True, spectra=["total"])["total"]
    out = cl[:, 0].copy(); out[:2] = 0.0
    return out


def cosmic_variance(ell, cl, fsky=1.0, nlb=1):
    """Cosmic-variance error on a (binned) C_ℓ: σ = √(2/((2ℓ+1) f_sky n_b)) · C_ℓ."""
    ell = np.asarray(ell, float)
    return np.sqrt(2.0 / ((2 * ell + 1) * fsky * nlb)) * np.asarray(cl, float)


def fit_cosmology(ell_data, cl_data, err, p0=None, lmax=2200, bounds=None):
    """Fit (H0, ωc, As) to map-derived TT bandpowers (raw C_ℓ in μK²)."""
    from scipy.optimize import minimize
    p0 = p0 or [FIDUCIAL["H0"], FIDUCIAL["omch2"], FIDUCIAL["As"]]
    bounds = bounds or [(60, 75), (0.10, 0.14), (1.8, 2.4)]
    ell_data = np.asarray(ell_data, float)
    cl_data = np.asarray(cl_data, float)
    err = np.asarray(err, float)

    def neg(x):
        if not all(lo <= v <= hi for v, (lo, hi) in zip(x, bounds)):
            return 1e10
        th = theory_cl_tt(x[0], x[1], x[2], lmax=lmax)
        model = np.interp(ell_data, np.arange(th.size), th)
        return float(np.sum(((cl_data - model) / err) ** 2))

    res = minimize(neg, p0, method="Nelder-Mead",
                   options={"xatol": 1e-3, "fatol": 0.5, "maxiter": 300})
    return dict(H0=float(res.x[0]), omch2=float(res.x[1]), As=float(res.x[2]),
                chi2=float(res.fun), ndof=len(ell_data) - 3, success=bool(res.success))
