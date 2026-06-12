"""Generate the demo's data: a power spectrum DECOMPOSED FROM A MAP.

We do NOT ship Planck's pre-binned spectra. Instead we build an observation from
scratch the way you actually would:

  1. pick a cosmology and get its theory C_ℓ from CAMB,
  2. synthesize a full-sky Gaussian CMB **map** at Nside 2048 (synfast),
  3. spherically-harmonic-decompose that map back into a power spectrum (our own
     map → a_ℓm → Ĉ_ℓ pipeline), correcting the pixel window, and bin it.

The Nside-2048 map is 50 million pixels (~400 MB) — too big to commit — so it is
regenerated deterministically from the seed here. The committed data product is the
small **bandpowers** CSV (the spectrum we measured off the map), plus params.json with
the input cosmology so the fit test can check recovery.

    python make_synthetic.py     # writes bandpowers_tt.csv, bandpowers_te.csv, params.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.powerspectrum import (generate_cmb_map, map_to_alm, cl_from_alm,
                                   pixel_window, bin_spectrum)
from scripts.cosmofit import theory_cl_tt, cosmic_variance

TRUTH = dict(H0=69.0, omch2=0.118, As=2.05, nside=2048, lmax=2000, nlb=40, seed=17)


def main():
    import healpy as hp
    import camb
    t = TRUTH
    pars = camb.set_params(H0=t["H0"], ombh2=0.02237, omch2=t["omch2"], ns=0.9649,
                           As=t["As"] * 1e-9, tau=0.0544, lmax=t["lmax"] + 300)
    spec = camb.get_results(pars).get_cmb_power_spectra(
        pars, CMB_unit="muK", raw_cl=True, spectra=["total"])["total"]
    # CAMB total columns: TT, EE, BB, TE
    cl_in = np.zeros((4, t["lmax"] + 1))
    for i in range(4):
        cl_in[i] = spec[:t["lmax"] + 1, i]
    cl_in[:, :2] = 0.0

    # --- synthesize a polarized Nside 2048 map and decompose it ---
    np.random.seed(t["seed"])
    maps = hp.synfast([cl_in[0], cl_in[1], cl_in[2], cl_in[3]], t["nside"],
                      lmax=t["lmax"], pol=True, new=True, pixwin=True)   # [T, Q, U]
    ell = np.arange(t["lmax"] + 1)
    pw_T, pw_P = hp.pixwin(t["nside"], lmax=t["lmax"], pol=True)

    # TT: OUR hand-rolled pipeline (map → a_ℓm → Ĉ_ℓ)
    alm_T = map_to_alm(maps[0], t["lmax"])
    cl_tt = cl_from_alm(alm_T, t["lmax"]) / pw_T ** 2
    l_tt, cb_tt = bin_spectrum(ell, cl_tt, lmin=30, lmax=t["lmax"], nlb=t["nlb"])

    # TE: the polarization cross-spectrum (spin-2 transform, via healpy)
    cls = hp.anafast(maps, lmax=t["lmax"], pol=True)             # TT,EE,BB,TE,EB,TB
    with np.errstate(invalid="ignore", divide="ignore"):
        cl_te = cls[3] / (pw_T * pw_P)
    cl_te[:2] = 0.0
    l_te, cb_te = bin_spectrum(ell, cl_te, lmin=30, lmax=t["lmax"], nlb=t["nlb"])

    # cosmic-variance error bars (one sky, full-sky here)
    e_tt = cosmic_variance(l_tt, cb_tt, fsky=1.0, nlb=t["nlb"])
    e_te = np.abs(cosmic_variance(l_te, np.abs(cb_te) + cb_tt[:len(cb_te)] * 0, 1.0, t["nlb"]))

    np.savetxt(HERE / "bandpowers_tt.csv", np.column_stack([l_tt, cb_tt, e_tt]),
               delimiter=",", header="ell,Cl_tt_muK2,dCl", comments="")
    np.savetxt(HERE / "bandpowers_te.csv", np.column_stack([l_te, cb_te, e_te]),
               delimiter=",", header="ell,Cl_te_muK2,dCl", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"decomposed a Nside={t['nside']} map ({maps[0].size} pixels) into "
          f"{len(l_tt)} TT + {len(l_te)} TE bandpowers; injected H0={t['H0']}")


if __name__ == "__main__":
    main()
