"""Two independent ways to trust the distance.

1. test_recovers_injected_distance — synthetic cluster at a KNOWN distance with noisy
   parallaxes; assert our parallax-first estimator recovers it. (A naive mean of 1/ϖ
   is biased here — this test would catch that mistake.)
2. test_conversion_matches_astropy — assert our parallax→distance conversion matches
   astropy.coordinates.Distance(parallax=...), the standard implementation.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cluster import cluster_distance, parallax_to_distance  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def test_recovers_injected_distance():
    arr = np.loadtxt(SYN / "cluster.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    d = cluster_distance(arr[:, 0], arr[:, 1])
    assert d == pytest.approx(truth["distance_pc"], rel=0.01)


def test_conversion_matches_astropy():
    u = pytest.importorskip("astropy.units")
    from astropy.coordinates import Distance
    import astropy.units as u
    for plx in [1.0, 7.37, 50.0, 100.0]:
        ours = parallax_to_distance(plx)
        ref = Distance(parallax=plx * u.mas).to("pc").value
        assert ours == pytest.approx(ref, rel=1e-6)
