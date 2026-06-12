"""Two independent ways to trust the cosmology fit.

1. test_recovers_injected_cosmology — fit mock TT+TE built from KNOWN parameters and
   assert we recover them. (A reduced 2-parameter fit at modest lmax, to stay fast.)
2. test_normalization_matches_camb — assert our theory D_ℓ equals CAMB's *raw* C_ℓ
   converted by hand with ℓ(ℓ+1)/2π and the μK² factor. This guards the classic CMB
   units trap (plotting C_ℓ instead of D_ℓ, or K instead of μK).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cmb import theory_spectrum, fit_cosmology, FIDUCIAL  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def _load_mock():
    tt = np.loadtxt(SYN / "mock_tt.csv", delimiter=",", skiprows=1)
    te = np.loadtxt(SYN / "mock_te.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    return {"tt": (tt[:, 0], tt[:, 1], tt[:, 2]),
            "te": (te[:, 0], te[:, 1], te[:, 2])}, truth


def test_recovers_injected_cosmology():
    pytest.importorskip("camb")
    data, truth = _load_mock()
    # fit at a modest lmax for speed; start at the Planck fiducial (offset from truth)
    fit = fit_cosmology(data, p0=[FIDUCIAL["H0"], FIDUCIAL["omch2"], FIDUCIAL["As"]],
                        lmax=2200)
    assert fit["H0"] == pytest.approx(truth["H0"], abs=1.5)
    assert fit["omch2"] == pytest.approx(truth["omch2"], abs=0.004)
    assert fit["As"] == pytest.approx(truth["As"], abs=0.08)


def test_normalization_matches_camb():
    camb = pytest.importorskip("camb")
    H0, omch2, As = 67.36, 0.120, 2.10
    ell, D_tt, _ = theory_spectrum(H0, omch2, As, lmax=2000)

    # independent path: raw (dimensionless) C_ℓ from CAMB, converted BY HAND
    pars = camb.set_params(H0=H0, ombh2=0.02237, omch2=omch2, ns=0.9649,
                           As=As * 1e-9, tau=0.0544, lmax=2000)
    res = camb.get_results(pars)
    raw = res.get_cmb_power_spectra(pars, CMB_unit=None, raw_cl=True,
                                    spectra=["total"])["total"]
    l = np.arange(raw.shape[0])
    T_cmb_muK = 2.7255e6
    with np.errstate(invalid="ignore"):
        D_manual = raw[:, 0] * l * (l + 1) / (2 * np.pi) * T_cmb_muK ** 2

    sel = slice(30, 2000)         # skip ℓ<2 where the factor is 0/undefined
    assert D_tt[sel] == pytest.approx(D_manual[sel], rel=1e-4)
