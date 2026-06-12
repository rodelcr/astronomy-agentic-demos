"""cmb.py — fit a ΛCDM cosmology to the Planck CMB power spectrum. STUB (step 1)."""
from __future__ import annotations

FIXED = dict(ombh2=0.02237, ns=0.9649, tau=0.0544)
FIDUCIAL = dict(H0=67.36, omch2=0.1200, As=2.100)


def theory_spectrum(H0, omch2, As, ombh2=FIXED["ombh2"], ns=FIXED["ns"], tau=FIXED["tau"], lmax=2600):
    raise NotImplementedError("implemented at step 3")


def bin_to_data(ell, D_theory, ell_data):
    raise NotImplementedError("implemented at step 3")


def chi2(H0, omch2, As, data, lmax=2600):
    raise NotImplementedError("implemented at step 3")


def fit_cosmology(data, p0=None, lmax=2600, bounds=None):
    raise NotImplementedError("implemented at step 3")


def load_planck(tt_csv, te_csv):
    raise NotImplementedError("implemented at step 3")
