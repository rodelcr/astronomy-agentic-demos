"""cmb.py — fit a ΛCDM cosmology to the Planck CMB power spectrum.

Importable AND runnable from the shell:

    from scripts.cmb import theory_spectrum, fit_cosmology
    python scripts/cmb.py --tt data/real/planck_tt_binned.csv --te data/real/planck_te_binned.csv

The theory spectrum is computed by **CAMB**, the standard Boltzmann code — we do NOT
re-derive the physics (that takes a Boltzmann solver). The student's job is the
*inference*: build a likelihood, fit cosmological parameters, and check the result
against Planck's published values. We validate our spectrum normalization (the
ℓ(ℓ+1)/2π and μK² conversions — the classic CMB units trap) against CAMB directly.

Simplifications (see notes/): a Gaussian likelihood on the *binned* public spectra with
diagonal errors (not the full Planck `plik` likelihood + covariance + nuisance
parameters); theory sampled at each bin's effective multipole by interpolation (no
bandpower windows); a reduced parameter set (H0, ωc, As) with ωb, ns, τ held at the
Planck fiducial. The result is close to, but not identical to, official Planck values.
"""
from __future__ import annotations

import argparse

import numpy as np

# Planck 2018 fiducial for the parameters we hold fixed
FIXED = dict(ombh2=0.02237, ns=0.9649, tau=0.0544)
# starting point / fiducial for the free parameters
FIDUCIAL = dict(H0=67.36, omch2=0.1200, As=2.100)   # As in units of 1e-9


def theory_spectrum(H0, omch2, As, ombh2=FIXED["ombh2"], ns=FIXED["ns"],
                    tau=FIXED["tau"], lmax=2600):
    """ΛCDM lensed D_ℓ = ℓ(ℓ+1)C_ℓ/2π in μK², for TT and TE, via CAMB.

    Returns (ell, D_TT, D_TE). `As` is in units of 1e-9.
    """
    import camb
    pars = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, ns=ns,
                           As=As * 1e-9, tau=tau, lmax=lmax)
    results = camb.get_results(pars)
    cl = results.get_cmb_power_spectra(pars, CMB_unit="muK", spectra=["total"])["total"]
    ell = np.arange(cl.shape[0])
    return ell, cl[:, 0], cl[:, 3]          # columns: TT, EE, BB, TE


def bin_to_data(ell, D_theory, ell_data):
    """Sample a theory curve at the binned data's effective multipoles (interpolation)."""
    return np.interp(np.asarray(ell_data, float), ell, D_theory)


def chi2(H0, omch2, As, data, lmax=2600):
    """Joint TT+TE Gaussian χ² of the theory against the binned Planck data.

    `data` is a dict with keys 'tt' and 'te', each (ell, Dl, dDl) arrays.
    """
    ell, D_tt, D_te = theory_spectrum(H0, omch2, As, lmax=lmax)
    chi = 0.0
    for key, model in (("tt", D_tt), ("te", D_te)):
        l, D, dD = data[key]
        m = bin_to_data(ell, model, l)
        chi += float(np.sum(((D - m) / dD) ** 2))
    return chi


def fit_cosmology(data, p0=None, lmax=2600, bounds=None):
    """Fit (H0, ωc, As) to the Planck data by minimizing the joint χ².

    Returns dict(H0, omch2, As, chi2, ndof, success).
    """
    from scipy.optimize import minimize
    p0 = p0 or [FIDUCIAL["H0"], FIDUCIAL["omch2"], FIDUCIAL["As"]]
    bounds = bounds or [(60, 75), (0.10, 0.14), (1.8, 2.4)]

    def neg(x):
        H0, omch2, As = x
        if not all(lo <= v <= hi for v, (lo, hi) in zip(x, bounds)):
            return 1e10
        return chi2(H0, omch2, As, data, lmax=lmax)

    res = minimize(neg, p0, method="Nelder-Mead",
                   options={"xatol": 1e-3, "fatol": 0.5, "maxiter": 300})
    n = sum(len(data[k][0]) for k in ("tt", "te"))
    return dict(H0=float(res.x[0]), omch2=float(res.x[1]), As=float(res.x[2]),
                chi2=float(res.fun), ndof=n - 3, success=bool(res.success))


def load_planck(tt_csv, te_csv):
    """Load the binned Planck TT and TE CSVs into the `data` dict chi2/fit expect."""
    tt = np.loadtxt(tt_csv, delimiter=",", skiprows=1)
    te = np.loadtxt(te_csv, delimiter=",", skiprows=1)
    return {"tt": (tt[:, 0], tt[:, 1], tt[:, 2]),
            "te": (te[:, 0], te[:, 1], te[:, 2])}


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tt", required=True, help="Planck TT binned CSV")
    p.add_argument("--te", required=True, help="Planck TE binned CSV")
    args = p.parse_args()
    data = load_planck(args.tt, args.te)
    fit = fit_cosmology(data)
    print(f"H0     = {fit['H0']:.2f} km/s/Mpc   (Planck 67.36)")
    print(f"omch2  = {fit['omch2']:.4f}         (Planck 0.1200)")
    print(f"As/1e-9= {fit['As']:.3f}            (Planck 2.100)")
    print(f"chi2   = {fit['chi2']:.1f} / {fit['ndof']} dof")


if __name__ == "__main__":
    _main()
