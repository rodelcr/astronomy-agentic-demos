"""Two independent ways to trust H0.

1. test_recovers_injected_H0 — fit synthetic data built from a KNOWN H0; assert the
   point estimate is close AND the bootstrap interval brackets the truth. (An error
   bar that misses the known answer is worse than useless.)
2. test_agrees_with_scipy — assert our closed-form through-origin slope matches a
   scipy curve_fit of v = H0·d. Closed form vs numerical optimizer: a real cross-check.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.hubble import fit_h0, bootstrap_h0  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def _load():
    arr = np.loadtxt(SYN / "hubble.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    return arr[:, 0], arr[:, 1], truth


def test_recovers_injected_H0():
    dist, vel, truth = _load()
    H0 = fit_h0(dist, vel)
    med, lo, hi = bootstrap_h0(dist, vel, n_boot=2000)
    assert H0 == pytest.approx(truth["H0"], rel=0.05)
    assert lo <= truth["H0"] <= hi            # the interval must bracket the truth


def test_agrees_with_scipy():
    scipy = pytest.importorskip("scipy")
    from scipy.optimize import curve_fit
    dist, vel, _ = _load()
    ours = fit_h0(dist, vel)
    (h_scipy,), _ = curve_fit(lambda d, H: H * d, dist, vel, p0=[70.0])
    assert ours == pytest.approx(h_scipy, rel=1e-6)
