"""fetch_real_map.py — rebuild the committed real-Planck files from the archive.

The demo ships a downgraded (Nside 256) Planck SMICA map + mask so the real-data check runs
offline. This script reproduces those files from the full-resolution archive product:

    python scripts/fetch_real_map.py        # downloads ~2 GB, writes data/real/*_nside256.fits

The full SMICA map is ~2 GB and the ESA archive throttles, so the download resumes on retry.
You only need this if you want to regenerate the committed files (or go to higher resolution).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
URL = ("https://pla.esac.esa.int/pla/aio/product-action?"
       "MAP.MAP_ID=COM_CMB_IQU-smica_2048_R3.00_full.fits")
RAW = PROJECT / "data" / "real" / "_smica_full.fits"
SIZE = 2013275520
NOUT = 256


def download():
    RAW.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 61):
        subprocess.run(["curl", "-sL", "-C", "-", "--max-time", "180", "-o", str(RAW), URL])
        if RAW.exists() and RAW.stat().st_size >= SIZE:
            print(f"download complete ({RAW.stat().st_size} bytes)")
            return
        print(f"attempt {attempt}: {RAW.stat().st_size if RAW.exists() else 0} / {SIZE} bytes")
    sys.exit("download did not complete — rerun to resume")


def downgrade():
    import healpy as hp
    import numpy as np
    I = hp.read_map(RAW, field=0) * 1e6          # I_STOKES, K -> μK
    mask = hp.read_map(RAW, field=3)             # TMASK
    hp.write_map(PROJECT / "data/real/planck_smica_I_nside256.fits",
                 hp.ud_grade(I, NOUT).astype(np.float32), overwrite=True, column_units="uK_CMB")
    hp.write_map(PROJECT / "data/real/planck_smica_mask_nside256.fits",
                 (hp.ud_grade(mask, NOUT) > 0.5).astype(np.float32), overwrite=True)
    print(f"wrote Nside-{NOUT} SMICA temperature + mask to data/real/")


if __name__ == "__main__":
    download()
    downgrade()
