"""powerspectrum.py — the CMB angular power spectrum from a sky MAP.

This is the heart of the demo: how you get a power spectrum out of a HEALPix map by
**spherical-harmonic decomposition**. A temperature map T(n̂) on the sphere is expanded
in spherical harmonics,

    a_ℓm = ∫ T(n̂) Y*_ℓm(n̂) dΩ          (computed here with healpy.map2alm),

and its angular power spectrum is the variance of those coefficients at each scale ℓ,

    Ĉ_ℓ = 1/(2ℓ+1) Σ_{m=-ℓ}^{ℓ} |a_ℓm|² .

`cl_from_alm` implements that m-sum **by hand** (HEALPix stores only m ≥ 0, so for a real
map the sum is |a_{ℓ0}|² + 2 Σ_{m≥1} |a_ℓm|²) so the estimator is visible, not hidden in a
library call — and we validate it against healpy.alm2cl.

Real skies are masked (the Galaxy is removed), which couples multipoles. The naive
`pseudo_cl` divides by f_sky = ⟨mask²⟩ as a first correction; the rigorous mode-coupling
("MASTER") deconvolution is done by **NaMaster** in `namaster_bandpowers`, which is our
external answer key for the masked case.

Importable AND runnable:

    from scripts.powerspectrum import map_to_alm, cl_from_alm, namaster_bandpowers
    python scripts/powerspectrum.py --nside 2048 --lmax 2000   # synth map -> spectrum
"""
from __future__ import annotations

import argparse

import numpy as np


# ---------------------------------------------------------------------------
# Making a sky to analyze (a Gaussian CMB realization from a theory spectrum)
# ---------------------------------------------------------------------------
def generate_cmb_map(cl, nside, lmax, seed, apply_pixwin=True):
    """Deterministic Gaussian CMB map (μK) drawn from a theory C_ℓ (μK²).

    By default the HEALPix pixel window is applied to the a_ℓm before pixelizing, so
    the map behaves like a real observation (finite pixels smooth small scales). The
    analysis then divides by pixwin² to undo it — an exact correction, not a bias.
    """
    import healpy as hp
    np.random.seed(seed)
    alm = hp.synalm(np.asarray(cl, float), lmax=lmax)
    if apply_pixwin:
        alm = hp.almxfl(alm, hp.pixwin(nside, lmax=lmax))
    return hp.alm2map(alm, nside, lmax=lmax)


# ---------------------------------------------------------------------------
# The spherical-harmonic decomposition
# ---------------------------------------------------------------------------
def map_to_alm(hmap, lmax):
    """Spherical-harmonic transform: T(n̂) → a_ℓm  (healpy.map2alm)."""
    import healpy as hp
    return hp.map2alm(np.asarray(hmap, float), lmax=lmax)


def cl_from_alm(alm, lmax=None):
    """Angular power spectrum from a_ℓm, BY HAND: Ĉ_ℓ = 1/(2ℓ+1) Σ_m |a_ℓm|².

    HEALPix stores only m ≥ 0; for a real field |a_{ℓ,-m}| = |a_{ℓm}|, so the full
    m-sum is |a_{ℓ0}|² + 2 Σ_{m=1}^{ℓ} |a_ℓm|². This is exactly what healpy.alm2cl
    returns — `test_cl_from_alm_matches_healpy` checks it.
    """
    import healpy as hp
    lmax = lmax if lmax is not None else hp.Alm.getlmax(alm.size)
    cl = np.zeros(lmax + 1)
    for ell in range(lmax + 1):
        idx = hp.Alm.getidx(lmax, ell, np.arange(0, ell + 1))
        p = np.abs(alm[idx]) ** 2
        cl[ell] = (p[0] + 2.0 * np.sum(p[1:])) / (2 * ell + 1)
    return cl


def pixel_window(nside, lmax):
    """HEALPix pixel window function w_ℓ (finite pixels smooth the map)."""
    import healpy as hp
    return hp.pixwin(nside, lmax=lmax)


def pseudo_cl(hmap, mask, lmax, nside, correct_pixwin=True):
    """Naive masked estimator: Ĉ_ℓ of (map·mask) divided by f_sky = ⟨mask²⟩.

    A first-order mask correction. It does NOT undo multipole mode-coupling — that's
    what NaMaster does; compare the two to see the difference.
    """
    alm = map_to_alm(np.asarray(hmap, float) * np.asarray(mask, float), lmax)
    cl = cl_from_alm(alm, lmax) / np.mean(np.asarray(mask, float) ** 2)
    if correct_pixwin:
        cl = cl / pixel_window(nside, lmax) ** 2
    return cl


def bin_spectrum(ell, cl, lmin=30, lmax=2000, nlb=40):
    """Bin a spectrum into bandpowers of width `nlb`. Returns (ℓ_eff, C_ℓ binned)."""
    ell = np.asarray(ell); cl = np.asarray(cl)
    edges = np.arange(lmin, lmax + 1, nlb)
    leff, binned = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (ell >= lo) & (ell < hi)
        if sel.any():
            leff.append(ell[sel].mean()); binned.append(cl[sel].mean())
    return np.array(leff), np.array(binned)


def namaster_bandpowers(hmap, mask, nside, nlb=40):
    """MASTER pseudo-C_ℓ with full mode-coupling deconvolution (NaMaster).

    The rigorous masked estimator — our external answer key. Returns (ℓ_eff, C_ℓ).
    """
    import pymaster as nmt
    f = nmt.NmtField(np.asarray(mask, float), [np.asarray(hmap, float)])
    b = nmt.NmtBin.from_nside_linear(nside, nlb)
    wk = nmt.NmtWorkspace()
    wk.compute_coupling_matrix(f, f, b)
    cl = wk.decouple_cell(nmt.compute_coupled_cell(f, f))[0]
    return b.get_effective_ells(), cl


def _main() -> None:
    import healpy as hp
    import camb
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nside", type=int, default=2048)
    p.add_argument("--lmax", type=int, default=2000)
    p.add_argument("--seed", type=int, default=17)
    args = p.parse_args()

    pars = camb.set_params(H0=67.36, ombh2=0.02237, omch2=0.12, ns=0.9649,
                           As=2.1e-9, tau=0.0544, lmax=args.lmax + 300)
    cl_th = camb.get_results(pars).get_cmb_power_spectra(
        pars, CMB_unit="muK", raw_cl=True, spectra=["total"])["total"][:args.lmax + 1, 0]
    cl_th[:2] = 0
    m = generate_cmb_map(cl_th, args.nside, args.lmax, args.seed)
    alm = map_to_alm(m, args.lmax)
    cl = cl_from_alm(alm, args.lmax) / pixel_window(args.nside, args.lmax) ** 2
    ell = np.arange(cl.size)
    leff, cb = bin_spectrum(ell, cl)
    print(f"map Nside={args.nside}, {m.size} pixels; decomposed to ℓ≤{args.lmax}")
    print(f"recovered {len(leff)} bandpowers; "
          f"⟨Ĉ/C_th⟩(200–1500) = "
          f"{np.mean(cb[(leff>200)&(leff<1500)]/np.interp(leff,ell,cl_th)[(leff>200)&(leff<1500)]):.3f}")


if __name__ == "__main__":
    _main()
