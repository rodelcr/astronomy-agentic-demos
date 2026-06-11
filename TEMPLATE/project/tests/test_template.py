"""Two tests, two independent ways to trust the result.

1. test_recovers_injected  — run on synthetic data, assert we get the KNOWN answer
                             from params.json (a ground-truth oracle).
2. test_agrees_with_<lib>  — run a canonical external library on the same data,
                             assert our result matches it within tolerance.

A result that passes both is one you can defend.
"""
import json
from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parents[1] / "data"


def test_recovers_injected():
    truth = json.loads((DATA / "synthetic" / "params.json").read_text())
    # result = measure(load(DATA / "synthetic" / ...))
    # assert result == pytest.approx(truth["<quantity>"], rel=...)
    pytest.skip("template — replace in a real demo")


def test_agrees_with_external_library():
    # ours = measure(load(DATA / "real" / ...))
    # reference = <library>(...)            # the answer key
    # assert ours == pytest.approx(reference, rel=...)
    pytest.skip("template — replace in a real demo")
