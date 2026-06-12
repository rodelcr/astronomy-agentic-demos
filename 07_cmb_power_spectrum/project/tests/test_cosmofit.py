"""Fit ΛCDM to the MAP-DERIVED bandpowers and recover the input cosmology.

The bandpowers in data/synthetic/ were measured off a Nside-2048 map by the
spherical-harmonic pipeline (see make_synthetic.py). This test fits a CAMB model to
them and checks we get back the cosmology that generated the map — closing the loop
map → spectrum → parameters.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cosmofit import fit_cosmology, FIDUCIAL  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def test_recovers_injected_cosmology():
    pytest.importorskip("camb")
    bp = np.loadtxt(SYN / "bandpowers_tt.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    # use ℓ < 1500 where cosmic variance is small and the map-derived spectrum is clean
    sel = bp[:, 0] < 1500
    fit = fit_cosmology(bp[sel, 0], bp[sel, 1], bp[sel, 2],
                        p0=[FIDUCIAL["H0"], FIDUCIAL["omch2"], FIDUCIAL["As"]], lmax=1800)
    assert fit["H0"] == pytest.approx(truth["H0"], abs=2.0)
    assert fit["omch2"] == pytest.approx(truth["omch2"], abs=0.005)
    assert fit["As"] == pytest.approx(truth["As"], abs=0.10)
