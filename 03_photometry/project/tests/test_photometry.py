"""Two independent ways to trust the photometry.

1. test_recovers_relative_photometry — measure synthetic stars of KNOWN flux; assert
   recovered magnitude DIFFERENCES match the true differences. (Aperture losses are
   common to all stars, so relative photometry is the honest, testable quantity.)
2. test_agrees_with_photutils — assert our hand-rolled aperture sum matches
   photutils' CircularAperture (method='center') on the same image and positions.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.photometry import aperture_flux_raw, measure, instrumental_mag  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def _load():
    img = np.load(SYN / "starfield.npy")
    truth = json.loads((SYN / "params.json").read_text())
    return img, truth


def test_recovers_relative_photometry():
    img, truth = _load()
    pos = [(s[0], s[1]) for s in truth["stars"]]
    true_flux = np.array([s[2] for s in truth["stars"]])
    res = measure(img, pos, r=6.0, r_in=10.0, r_out=15.0)

    true_mag = instrumental_mag(true_flux)
    # compare magnitudes relative to the first star (cancels aperture loss + ZP)
    dm_meas = res["mag"] - res["mag"][0]
    dm_true = true_mag - true_mag[0]
    assert dm_meas == pytest.approx(dm_true, abs=0.02)


def test_agrees_with_photutils():
    photutils = pytest.importorskip("photutils")
    from photutils.aperture import CircularAperture, aperture_photometry
    img, truth = _load()
    pos = [(s[0], s[1]) for s in truth["stars"]]
    r = 6.0

    ours = np.array([aperture_flux_raw(img, x, y, r) for x, y in pos])
    ap = CircularAperture(pos, r=r)
    ref = aperture_photometry(img, ap, method="center")["aperture_sum"].data
    # 'center' counts whole pixels whose center is inside — same rule we use
    assert ours == pytest.approx(ref, rel=1e-6)
