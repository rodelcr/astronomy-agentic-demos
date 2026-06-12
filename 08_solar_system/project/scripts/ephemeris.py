"""ephemeris.py — planetary positions from a JPL ephemeris, and the physics they encode.

Importable AND runnable from the shell:

    from scripts.ephemeris import heliocentric_ecliptic, orbital_period
    python scripts/ephemeris.py --date 2026-06-12

We load JPL's definitive DE440 ephemeris with Skyfield, compute each planet's
**heliocentric, J2000-ecliptic** position (geometric — no light-time), and recover the
orbital period and semi-major axis straight from those positions. The positions are
validated against the independent JPL Horizons service; the periods/Kepler's third law are
the physics truth-oracle.

STUB — functions raise NotImplementedError until step 3/4 fill them in.
"""
from __future__ import annotations

import argparse
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
KERNEL = PROJECT / "data" / "kernels" / "de440s.bsp"

# Body -> (JPL/NAIF target id, rough search horizon in days ~1.2x the true period).
# Earth uses 399 (Earth centre, not the Earth-Moon barycentre) to avoid a monthly wobble;
# the search horizon only *sizes* the window — the recovered period is exact (see step 4).
BODIES = {
    "mercury": (1, 105.6),
    "venus": (2, 269.7),
    "earth": (399, 438.3),
    "mars": (4, 824.0),
    "jupiter": (5, 5198.0),
    "saturn": (6, 12910.0),
    "uranus": (7, 36850.0),
    "neptune": (8, 72260.0),
}


def heliocentric_ecliptic(body, t):
    """Geometric heliocentric position of `body` at Skyfield time `t`, AU, J2000 ecliptic.

    Returns an (x, y, z) numpy array (or (3, N) for an array of times).
    """
    raise NotImplementedError


def planet_position(body, t):
    """Alias kept for the CLI/viewer: same as heliocentric_ecliptic."""
    raise NotImplementedError


def orbital_period(body):
    """Sidereal orbital period of `body` in days, recovered from the ephemeris."""
    raise NotImplementedError


def semi_major_axis(body):
    """Semi-major axis of `body` in AU, recovered as (r_min + r_max)/2 over one orbit."""
    raise NotImplementedError


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", default="2026-06-12", help="UTC date YYYY-MM-DD")
    p.parse_args()
    raise SystemExit("ephemeris.py is a stub — implemented in step 3/4.")


if __name__ == "__main__":
    _main()
