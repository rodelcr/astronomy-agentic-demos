"""Two independent ways to trust the temperature.

1. test_recovers_injected_temperature — fit a synthetic blackbody of KNOWN temperature
   and assert we get it back.
2. test_planck_matches_astropy — assert our Planck function has the same SHAPE as
   astropy.modeling.BlackBody (the standard implementation) across the band.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.blackbody import planck_MJy, fit_temperature  # noqa: E402

SYN = PROJECT / "data" / "synthetic"


def test_recovers_injected_temperature():
    arr = np.loadtxt(SYN / "spectrum.csv", delimiter=",", skiprows=1)
    truth = json.loads((SYN / "params.json").read_text())
    T, T_err = fit_temperature(arr[:, 0], arr[:, 1], arr[:, 2])
    assert T == pytest.approx(truth["temperature"], rel=0.01)


def test_planck_matches_astropy():
    pytest.importorskip("astropy")
    from astropy.modeling.models import BlackBody
    import astropy.units as u

    freq_icm = np.linspace(2.0, 21.0, 50)
    T = 2.725
    ours = planck_MJy(freq_icm, T)

    nu = (freq_icm / u.cm).to(u.Hz, equivalencies=u.spectral())
    ref = BlackBody(temperature=T * u.K)(nu).to(
        u.MJy / u.sr, equivalencies=u.spectral_density(nu)).value

    # absolute radiance should match to high precision (both are B_ν in MJy/sr)
    assert ours == pytest.approx(ref, rel=1e-4)
