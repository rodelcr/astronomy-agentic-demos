"""ephemeris.py — planetary positions from a JPL ephemeris, and the physics they encode.

Importable AND runnable from the shell:

    from scripts.ephemeris import heliocentric_ecliptic, orbital_period
    python scripts/ephemeris.py --date 2026-06-12

We load JPL's definitive DE440 ephemeris with Skyfield, compute each planet's
**heliocentric, J2000-ecliptic** position (geometric — no light-time), and recover the
orbital period and semi-major axis straight from those positions. The positions are
validated against the independent JPL Horizons service; the periods/Kepler's third law are
the physics truth-oracle.

orbital_period / semi_major_axis are filled in at step 4.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
KERNEL = PROJECT / "data" / "kernels" / "de440s.bsp"

# IAU76 mean obliquity of the ecliptic at J2000.0 = 84381.448 arcsec. Rotating the ICRF
# (equatorial) vector about the x-axis by this angle gives the J2000 ecliptic frame that
# JPL Horizons reports (refplane='ecliptic'). Skyfield's built-in ecliptic_frame uses a
# slightly different equinox and disagrees by ~14 arcsec — see notes/TRANSCRIPT.
EPS_J2000 = np.radians(84381.448 / 3600.0)

# ordered for display (Sun-outward)
PLANETS = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]

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


_CACHE = {}


def _load():
    """Lazily load (and cache) the Skyfield timescale + DE440 ephemeris."""
    if "eph" not in _CACHE:
        from skyfield.api import load, load_file
        _CACHE["ts"] = load.timescale()
        _CACHE["eph"] = load_file(str(KERNEL))
    return _CACHE["ts"], _CACHE["eph"]


def _equatorial_to_ecliptic(xyz):
    """Rotate an ICRF (equatorial) vector into the J2000 ecliptic frame (about +x by ε)."""
    c, s = np.cos(EPS_J2000), np.sin(EPS_J2000)
    R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
    return R @ np.asarray(xyz, float)


def heliocentric_ecliptic(body, t):
    """Geometric heliocentric position of `body` at Skyfield time `t`, AU, J2000 ecliptic.

    Returns an (x, y, z) array (or (3, N) for an array of times). Geometric = no light-time
    or aberration, so it matches JPL Horizons geometric vectors to machine precision.
    """
    _, eph = _load()
    nid = BODIES[body][0]
    equ = (eph[nid] - eph[10]).at(t).position.au      # body − Sun, ICRF equatorial, AU
    return _equatorial_to_ecliptic(equ)


def planet_position(body, t):
    """Alias kept for the CLI/viewer: same as heliocentric_ecliptic."""
    return heliocentric_ecliptic(body, t)


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
    args = p.parse_args()
    y, m, d = (int(v) for v in args.date.split("-"))
    ts, _ = _load()
    t = ts.utc(y, m, d)
    print(f"Heliocentric ecliptic configuration on {args.date} (J2000 ecliptic):")
    print(f"  {'body':9s} {'r (AU)':>9s} {'ecl. lon (deg)':>15s}")
    for name in PLANETS:
        x, y_, z = heliocentric_ecliptic(name, t)
        r = float(np.hypot(np.hypot(x, y_), z))
        lon = float(np.degrees(np.arctan2(y_, x))) % 360.0
        print(f"  {name:9s} {r:9.3f} {lon:15.2f}")


if __name__ == "__main__":
    _main()
