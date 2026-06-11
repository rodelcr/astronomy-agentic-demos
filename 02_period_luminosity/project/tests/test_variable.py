"""Two independent ways to trust the period.

1. test_recovers_injected_period — run the string-length finder on synthetic data
   built from a KNOWN period; assert we recover it.
2. test_agrees_with_lombscargle  — assert our (string-length) period matches
   astropy's Lomb-Scargle on the same data. Two architecturally independent methods
   agreeing is strong evidence the period is real, not a method artifact.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.variable import string_length_period, lombscargle_period  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def _load_synthetic():
    arr = np.loadtxt(SYN / "lightcurve.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    return arr[:, 0], arr[:, 1], arr[:, 2], truth


def test_recovers_injected_period():
    time, mag, mag_err, truth = _load_synthetic()
    P, _, _ = string_length_period(time, mag, pmin=2.0, pmax=6.0, n_periods=8000)
    assert P == pytest.approx(truth["period"], rel=0.01)


def test_agrees_with_lombscargle():
    time, mag, mag_err, truth = _load_synthetic()
    P_sl, _, _ = string_length_period(time, mag, pmin=2.0, pmax=6.0, n_periods=8000)
    P_ls = lombscargle_period(time, mag, mag_err, pmin=2.0, pmax=6.0)
    assert P_sl == pytest.approx(P_ls, rel=0.01)
