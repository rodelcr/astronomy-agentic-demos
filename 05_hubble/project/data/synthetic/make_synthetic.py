"""Generate a synthetic Hubble diagram with a KNOWN H0.

Galaxies at random distances recede at v = H0·d, plus a **peculiar velocity** scatter
(real galaxies have their own motions on top of the Hubble flow). Seeded, with the
true H0 in params.json so the test checks both the point estimate and that the
bootstrap interval brackets the truth.

    python make_synthetic.py     # writes hubble.csv + params.json here
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

TRUTH = dict(
    H0=70.0,                 # km/s/Mpc — the answer key
    n_galaxies=200,
    dist_min=10.0,           # Mpc
    dist_max=200.0,
    peculiar_velocity=300.0, # km/s scatter (typical)
    seed=5,
)


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    dist = rng.uniform(t["dist_min"], t["dist_max"], t["n_galaxies"])
    vel = t["H0"] * dist + rng.normal(0.0, t["peculiar_velocity"], t["n_galaxies"])

    out = np.column_stack([dist, vel])
    np.savetxt(HERE / "hubble.csv", out, delimiter=",",
               header="dist_mpc,vel_kms", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {t['n_galaxies']} galaxies; injected H0 = {t['H0']} km/s/Mpc")


if __name__ == "__main__":
    main()
