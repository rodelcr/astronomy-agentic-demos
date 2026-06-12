"""Generate mock CMB TT+TE spectra from a KNOWN cosmology.

We pick cosmological parameters, compute the theory spectra with CAMB, sample them at
the same multipoles as the real Planck bins, and add Gaussian noise scaled to the real
Planck error bars. The injected parameters go in params.json, so the test can check we
recover them. Seeded → reproducible.

    python make_synthetic.py     # writes mock_tt.csv, mock_te.csv, params.json here
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.cmb import theory_spectrum, bin_to_data, load_planck

TRUTH = dict(H0=69.0, omch2=0.118, As=2.05, seed=17)   # deliberately off Planck fiducial


def main():
    # reuse the real bins' multipoles + error bars as the mock's noise model
    real = load_planck(PROJECT / "data" / "real" / "planck_tt_binned.csv",
                       PROJECT / "data" / "real" / "planck_te_binned.csv")
    rng = np.random.default_rng(TRUTH["seed"])
    ell, D_tt, D_te = theory_spectrum(TRUTH["H0"], TRUTH["omch2"], TRUTH["As"])

    for key, model, fname in (("tt", D_tt, "mock_tt.csv"), ("te", D_te, "mock_te.csv")):
        l, _, dD = real[key]
        clean = bin_to_data(ell, model, l)
        noisy = clean + rng.normal(0.0, dD)
        out = np.column_stack([l, noisy, dD])
        np.savetxt(HERE / fname, out, delimiter=",",
                   header="ell,Dl_muK2,dDl_muK2", comments="")
    (HERE / "params.json").write_text(json.dumps(TRUTH, indent=2))
    print(f"wrote mock TT+TE at H0={TRUTH['H0']}, omch2={TRUTH['omch2']}, As={TRUTH['As']}")


if __name__ == "__main__":
    main()
