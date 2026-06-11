"""Two independent ways to trust Rp/R*.

1. test_recovers_injected_depth — fit the synthetic light curve (built from a KNOWN
   depth) and check we get that depth back. A ground-truth oracle.
2. test_agrees_with_batman      — generate a transit with the canonical `batman`
   model (uniform source, so depth = (Rp/R*)^2 exactly) and check our estimator
   recovers batman's input Rp/R*.

A number that passes both is one you can defend.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.transit import fit_transit, rp_over_rstar  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def _load_synthetic():
    arr = np.loadtxt(SYN / "lightcurve.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    return arr[:, 0], arr[:, 1], arr[:, 2], truth


def test_recovers_injected_depth():
    time, flux, flux_err, truth = _load_synthetic()
    res = fit_transit(time, flux, flux_err, period=truth["period"], t0=truth["t0"])
    assert res["depth"] == pytest.approx(truth["depth"], rel=0.05)
    assert res["rp_over_rstar"] == pytest.approx(truth["rp_over_rstar"], rel=0.05)


def test_agrees_with_batman():
    batman = pytest.importorskip("batman")
    # A transit with a UNIFORM source: limb darkening off, so depth = rp^2 exactly.
    rp_true = 0.1
    period, t0 = 3.0, 1.0
    params = batman.TransitParams()
    params.t0 = t0
    params.per = period
    params.rp = rp_true
    params.a = 12.0
    params.inc = 90.0
    params.ecc = 0.0
    params.w = 90.0
    params.u = []            # no limb-darkening coefficients...
    params.limb_dark = "uniform"   # ...uniform stellar disk
    time = np.linspace(0.0, period, 2000)
    model = batman.TransitModel(params, time)
    flux = model.light_curve(params)
    flux_err = np.full_like(flux, 1e-4)

    res = fit_transit(time, flux, flux_err, period=period, t0=t0)
    assert res["rp_over_rstar"] == pytest.approx(rp_true, rel=0.03)
    # and our standalone helper inverts the geometry correctly
    assert rp_over_rstar(rp_true**2) == pytest.approx(rp_true, rel=1e-6)
