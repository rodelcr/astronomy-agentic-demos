"""Render the inspection figures for the CMB map → power-spectrum demo.

    python scripts/make_figures.py     # regenerates the map, runs the pipeline, writes results/

Figures:
  - map_and_spectrum.png : the synthetic Nside-2048 sky (Mollweide) + the power spectrum
                           we decomposed out of it, over the input theory.
  - masking_namaster.png : masked sky — our naive fsky estimator vs NaMaster's MASTER.
  - cosmology_fit.png    : ΛCDM best-fit to the map-derived TT+TE bandpowers.
  - real_smica.png       : the real Planck SMICA map (Nside 256) + its spectrum.
The fit's best-fit parameters are cached to results/best_fit.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import healpy as hp

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.powerspectrum import (generate_cmb_map, map_to_alm, cl_from_alm,  # noqa: E402
                                   pixel_window, pseudo_cl, bin_spectrum, namaster_bandpowers)
from scripts.cosmofit import theory_cl_tt, theory_spectrum, fit_cosmology  # noqa: E402

LMAX, NSIDE, SEED, NLB = 2000, 2048, 17, 40
TRUTH = dict(H0=69.0, omch2=0.118, As=2.05)


def _dl(ell, cl):
    ell = np.asarray(ell, float)
    return ell * (ell + 1) * cl / (2 * np.pi)


def main():
    res = PROJECT / "results"
    cl_in = theory_cl_tt(TRUTH["H0"], TRUTH["omch2"], TRUTH["As"], lmax=LMAX)[:LMAX + 1]
    m = generate_cmb_map(cl_in, NSIDE, LMAX, SEED)
    cl_rec = cl_from_alm(map_to_alm(m, LMAX), LMAX) / pixel_window(NSIDE, LMAX) ** 2
    ell = np.arange(LMAX + 1)
    l_eff, cb = bin_spectrum(ell, cl_rec, 30, LMAX, NLB)

    # 1. map + spectrum
    fig = plt.figure(figsize=(12, 4.5))
    plt.axes([0.02, 0.05, 0.46, 0.9])
    hp.mollview(m, title="synthetic CMB sky (Nside 2048)", unit="μK", cmap="RdBu_r",
                min=-300, max=300, hold=True, cbar=True)
    ax = fig.add_axes([0.57, 0.13, 0.40, 0.78])
    ax.plot(ell, _dl(ell, cl_in), "-", color="0.6", lw=1, label="input theory")
    ax.plot(l_eff, _dl(l_eff, cb), "o", ms=4, color="crimson", label="decomposed from the map")
    ax.set_xlim(0, LMAX); ax.set_xlabel("multipole ℓ"); ax.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ (\mu K^2)$")
    ax.set_title("map → spherical harmonics → power spectrum"); ax.legend(fontsize=8)
    fig.savefig(res / "map_and_spectrum.png", dpi=120, bbox_inches="tight")
    plt.close("all")

    # 2. masking + NaMaster (smaller Nside for speed)
    ns2, lmax2 = 1024, 1500
    m2 = generate_cmb_map(theory_cl_tt(TRUTH["H0"], TRUTH["omch2"], TRUTH["As"], lmax=lmax2),
                          ns2, lmax2, SEED)
    import pymaster as nmt
    b_gal = 90 - np.degrees(hp.pix2ang(ns2, np.arange(hp.nside2npix(ns2)))[0])
    mask = nmt.mask_apodization((np.abs(b_gal) > 15).astype(float), 2.0, apotype="C2")
    cl_naive = pseudo_cl(m2, mask, lmax2, ns2)
    ln, cbn = bin_spectrum(np.arange(lmax2 + 1), cl_naive, 30, lmax2, NLB)
    lm, cbm = namaster_bandpowers(m2, mask, ns2, NLB)
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    ax2.plot(ln, _dl(ln, cbn), "o", ms=4, color="orange", label="naive Ĉ_ℓ / f_sky")
    ax2.plot(lm, _dl(lm, cbm), "s", ms=4, mfc="none", color="crimson", label="NaMaster (MASTER)")
    ax2.set_xlim(0, lmax2); ax2.set_xlabel("multipole ℓ"); ax2.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ (\mu K^2)$")
    ax2.set_title("masked sky: naive f_sky vs NaMaster mode-coupling deconvolution")
    ax2.legend(fontsize=8)
    fig2.savefig(res / "masking_namaster.png", dpi=120, bbox_inches="tight")
    plt.close("all")

    # 3. cosmology fit to the map-derived bandpowers
    bp_tt = np.loadtxt(PROJECT / "data/synthetic/bandpowers_tt.csv", delimiter=",", skiprows=1)
    bp_te = np.loadtxt(PROJECT / "data/synthetic/bandpowers_te.csv", delimiter=",", skiprows=1)
    sel = bp_tt[:, 0] < 1500
    fit = fit_cosmology(bp_tt[sel, 0], bp_tt[sel, 1], bp_tt[sel, 2], lmax=1800)
    (res / "best_fit.json").write_text(json.dumps(fit, indent=2))
    ellf, Dtt, Dte = theory_spectrum(fit["H0"], fit["omch2"], fit["As"])
    fig3, (a0, a1) = plt.subplots(1, 2, figsize=(12, 4.2))
    a0.plot(ellf, Dtt, "-", color="crimson"); a0.errorbar(bp_tt[:, 0], _dl(bp_tt[:, 0], bp_tt[:, 1]),
            yerr=_dl(bp_tt[:, 0], bp_tt[:, 2]), fmt="o", ms=3, color="0.2")
    a0.set_xlim(0, 2000); a0.set_title(f"TT  (fit H₀={fit['H0']:.1f}, truth {TRUTH['H0']})")
    a0.set_xlabel("ℓ"); a0.set_ylabel(r"$\mathcal{D}_\ell\ (\mu K^2)$")
    a1.plot(ellf, Dte, "-", color="crimson"); a1.errorbar(bp_te[:, 0], _dl(bp_te[:, 0], bp_te[:, 1]),
            yerr=_dl(bp_te[:, 0], bp_te[:, 2]), fmt="o", ms=3, color="0.2")
    a1.set_xlim(0, 2000); a1.set_title("TE (polarization cross-spectrum)"); a1.set_xlabel("ℓ")
    fig3.savefig(res / "cosmology_fit.png", dpi=120, bbox_inches="tight")
    plt.close("all")

    # 4. real SMICA map + spectrum (if present)
    smica = PROJECT / "data/real/planck_smica_I_nside256.fits"
    if smica.exists():
        I = hp.read_map(smica); msk = hp.read_map(PROJECT / "data/real/planck_smica_mask_nside256.fits")
        lmax_r = 500
        clr = pseudo_cl(I, nmt.mask_apodization(msk, 5.0, "C2"), lmax_r, 256)
        lr, cbr = bin_spectrum(np.arange(lmax_r + 1), clr, 30, lmax_r, 30)
        fig4 = plt.figure(figsize=(12, 4.5))
        plt.axes([0.02, 0.05, 0.46, 0.9])
        hp.mollview(I * msk, title="real Planck SMICA (Nside 256, masked)", unit="μK",
                    cmap="RdBu_r", min=-300, max=300, hold=True)
        ax4 = fig4.add_axes([0.57, 0.13, 0.40, 0.78])
        ax4.plot(lr, _dl(lr, cbr), "o", ms=4, color="crimson", label="our pipeline on SMICA")
        ax4.plot(ellf, Dtt, "-", color="0.6", lw=1, label="Planck ΛCDM (reference)")
        ax4.set_xlim(0, lmax_r); ax4.set_xlabel("ℓ"); ax4.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ (\mu K^2)$")
        ax4.set_title("real CMB sky, decomposed"); ax4.legend(fontsize=8)
        fig4.savefig(res / "real_smica.png", dpi=120, bbox_inches="tight")
        plt.close("all")
        print("real SMICA figure written")

    print(f"fit H0={fit['H0']:.2f} (truth {TRUTH['H0']}), omch2={fit['omch2']:.4f}, "
          f"As={fit['As']:.3f}, chi2/dof={fit['chi2']/fit['ndof']:.2f}; figures written")


if __name__ == "__main__":
    main()
