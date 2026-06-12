"""Two independent ways to trust the orrery.

1. test_matches_horizons — our Skyfield heliocentric-ecliptic positions agree with cached
   **JPL Horizons** geometric vectors at fixed epochs (validates our frame/light-time usage).
2. test_recovers_orbital_periods / test_kepler_third_law — recover the known orbital periods
   and Kepler's third law (P^2 proportional to a^3) straight from the ephemeris (the
   independent *physics* oracle).

Horizons and Skyfield share the same JPL ephemeris, so (1) checks our *usage*, not the model;
(2) is the genuinely independent physics check.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.ephemeris import (  # noqa: E402
    heliocentric_ecliptic, orbital_period, semi_major_axis, BODIES,
)

REF = PROJECT / "data" / "reference"

# known sidereal periods (days) and semi-major axes (AU) — the literature truth we recover
PERIOD_TRUE = {"earth": 365.256, "mars": 686.98, "jupiter": 4332.59, "saturn": 10759.22}
A_TRUE = {"earth": 1.0000, "mars": 1.5237, "jupiter": 5.2026, "saturn": 9.5549}


def _load_horizons():
    """All cached Horizons reference rows: body, jd_tdb, x_au, y_au, z_au (helio ecliptic)."""
    rows = []
    for f in sorted(REF.glob("horizons_*.csv")):
        with open(f) as fh:
            next(fh)  # header
            for line in fh:
                body, jd, x, y, z = line.strip().split(",")
                rows.append((body, float(jd), float(x), float(y), float(z)))
    return rows


def test_matches_horizons():
    """Skyfield positions match the independent JPL Horizons service at sample epochs."""
    pytest.importorskip("skyfield")
    from skyfield.api import load
    ts = load.timescale()
    rows = _load_horizons()
    assert rows, "no Horizons reference CSVs — run scripts/fetch_kernel.py"
    for body, jd_tdb, x, y, z in rows:
        t = ts.tdb_jd(jd_tdb)
        ours = np.asarray(heliocentric_ecliptic(body, t), float)
        ref = np.array([x, y, z])
        # geometric positions from the same ephemeris should match very tightly
        assert np.linalg.norm(ours - ref) < 1e-3, f"{body}: {ours} vs {ref}"


@pytest.mark.parametrize("body", ["earth", "mars", "jupiter", "saturn"])
def test_recovers_orbital_periods(body):
    """Recover each planet's sidereal period from the ephemeris within ~1%."""
    pytest.importorskip("skyfield")
    P = orbital_period(body)
    assert P == pytest.approx(PERIOD_TRUE[body], rel=0.01)


def test_kepler_third_law():
    """P^2 (yr) proportional to a^3 (AU): the ratio is ~1 across the planets (Kepler III)."""
    pytest.importorskip("skyfield")
    bodies = ["earth", "mars", "jupiter", "saturn"]
    P_yr = np.array([orbital_period(b) for b in bodies]) / 365.25
    a_au = np.array([semi_major_axis(b) for b in bodies])
    ratio = P_yr ** 2 / a_au ** 3
    # in solar units P^2 = a^3 exactly, so every ratio is ~1
    assert np.allclose(ratio, 1.0, rtol=0.03), ratio
