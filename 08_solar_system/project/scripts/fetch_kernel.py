"""fetch_kernel.py — get the demo's data straight from JPL.

Two products, both fetched **directly from NASA/JPL** and committed so the demo runs
offline:

  1. data/kernels/de440s.bsp                — JPL's DE440 planetary ephemeris from NAIF (~31 MB)
  2. data/reference/horizons_positions.csv  — geometric heliocentric-ecliptic positions from
     the independent JPL **Horizons** service; the offline test oracle.

    python scripts/fetch_kernel.py            # downloads the kernel + rebuilds the CSV

The kernel download resumes on retry. You only need this to regenerate the committed files —
the demo ships them.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
KERNEL_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
KERNEL = PROJECT / "data" / "kernels" / "de440s.bsp"
KERNEL_SIZE = 32726016  # bytes, from the NAIF Content-Length

# Horizons reference: body name -> NAIF id (matches scripts/ephemeris.BODIES). Barycenters
# for Mars+ (de440s ships no planet-centre kernels for them); Earth uses 399 (not the EMB).
REF_BODIES = {"mercury": 1, "venus": 2, "earth": 399, "mars": 4, "jupiter": 5, "saturn": 6}
REF_DATES = ["2000-01-01", "2010-06-15", "2026-06-12"]   # spread across the kernel span


def download_kernel():
    KERNEL.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 31):
        subprocess.run(["curl", "-sL", "-C", "-", "--max-time", "300", "-o", str(KERNEL), KERNEL_URL])
        if KERNEL.exists() and KERNEL.stat().st_size >= KERNEL_SIZE:
            print(f"kernel complete ({KERNEL.stat().st_size} bytes)")
            return
        print(f"attempt {attempt}: {KERNEL.stat().st_size if KERNEL.exists() else 0} / {KERNEL_SIZE} bytes")
    sys.exit("kernel download did not complete — rerun to resume")


def cache_horizons():
    """Cache geometric heliocentric-ecliptic vectors from JPL Horizons (TDB, AU)."""
    from astropy.time import Time
    from astroquery.jplhorizons import Horizons
    out = PROJECT / "data" / "reference" / "horizons_positions.csv"
    jds = list(Time(REF_DATES, scale="tdb").jd)
    lines = ["body,jd_tdb,x_au,y_au,z_au"]
    for name, nid in REF_BODIES.items():
        obj = Horizons(id=str(nid), location="@sun", epochs=jds)
        v = obj.vectors(refplane="ecliptic")          # geometric, heliocentric, J2000 ecliptic
        for row in v:
            lines.append(f"{name},{float(row['datetime_jd']):.8f},"
                         f"{float(row['x']):.10f},{float(row['y']):.10f},{float(row['z']):.10f}")
        print(f"{name:8s} id={nid} -> {str(v['targetname'][0])}")
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {len(lines) - 1} rows to {out.relative_to(PROJECT)}")


if __name__ == "__main__":
    download_kernel()
    cache_horizons()
