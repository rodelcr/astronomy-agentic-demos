"""The spherical-harmonic pipeline, validated three ways.

1. test_cl_from_alm_matches_healpy — our BY-HAND estimator Ĉ_ℓ = 1/(2ℓ+1)Σ_m|a_ℓm|²
   reproduces healpy.alm2cl exactly. (The decomposition is real code, not a black box.)
2. test_recovers_input_spectrum — synthesize a map from a KNOWN C_ℓ, decompose it back,
   and recover the input within cosmic variance. (The pipeline is unbiased.)
3. test_namaster_agreement — on a MASKED sky, our fsky-corrected estimator agrees with
   NaMaster's rigorous MASTER deconvolution. (NaMaster is the external answer key.)
"""
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.powerspectrum import (generate_cmb_map, map_to_alm, cl_from_alm,  # noqa: E402
                                   pixel_window, pseudo_cl, bin_spectrum,
                                   namaster_bandpowers)


def _toy_cl(lmax):
    ell = np.arange(lmax + 1.0)
    cl = np.zeros(lmax + 1)
    cl[2:] = 1e4 * (ell[2:] / 200.0) ** -2 / (ell[2:] * (ell[2:] + 1) / (2 * np.pi))
    return cl


def test_cl_from_alm_matches_healpy():
    hp = pytest.importorskip("healpy")
    m = generate_cmb_map(_toy_cl(400), nside=256, lmax=300, seed=1)
    alm = map_to_alm(m, lmax=300)
    assert np.allclose(cl_from_alm(alm, 300), hp.alm2cl(alm), atol=1e-10)


def test_recovers_input_spectrum():
    pytest.importorskip("healpy")
    lmax, nside = 1200, 1024
    cl_in = _toy_cl(lmax)
    m = generate_cmb_map(cl_in, nside=nside, lmax=lmax, seed=2)
    cl_rec = cl_from_alm(map_to_alm(m, lmax), lmax) / pixel_window(nside, lmax) ** 2
    ell = np.arange(lmax + 1)
    l_eff, cb = bin_spectrum(ell, cl_rec, lmin=100, lmax=900, nlb=50)
    # bin the INPUT the same way (comparing to the theory value at bin center would add
    # a spurious bias for a steeply falling spectrum — that's binning, not the pipeline)
    _, cb_in = bin_spectrum(ell, cl_in, lmin=100, lmax=900, nlb=50)
    # binned recovery should be unbiased to a few percent (cosmic variance averaged down)
    assert np.mean(cb / cb_in) == pytest.approx(1.0, abs=0.05)


def test_namaster_agreement():
    hp = pytest.importorskip("healpy")
    nmt = pytest.importorskip("pymaster")
    lmax, nside, nlb = 700, 512, 40
    cl_in = _toy_cl(lmax)
    m = generate_cmb_map(cl_in, nside=nside, lmax=lmax, seed=3)
    npix = hp.nside2npix(nside)
    b_gal = 90 - np.degrees(hp.pix2ang(nside, np.arange(npix))[0])
    mask = nmt.mask_apodization((np.abs(b_gal) > 15).astype(float), 2.0, apotype="C2")

    cl_naive = pseudo_cl(m, mask, lmax, nside)
    l_eff_n, cb_naive = bin_spectrum(np.arange(lmax + 1), cl_naive, 100, 600, nlb)
    l_eff_m, cb_master = namaster_bandpowers(m, mask, nside, nlb)
    cb_master = np.interp(l_eff_n, l_eff_m, cb_master)
    # fsky-corrected and MASTER agree to ~10% (the residual is the mode-coupling)
    assert np.mean(cb_naive / cb_master) == pytest.approx(1.0, abs=0.10)
