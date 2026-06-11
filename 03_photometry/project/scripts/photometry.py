"""photometry.py — aperture photometry on an image: measure star brightnesses.

Importable AND runnable from the shell:

    from scripts.photometry import aperture_flux, instrumental_mag
    python scripts/photometry.py --image data/real/m67_cutout.fits

We do it by hand to expose the idea: a star's brightness is the sum of its pixels in
a circular **aperture**, minus the **sky** background estimated from a surrounding
**annulus**. Then instrumental magnitude = ZP − 2.5 log₁₀(net counts). The result is
validated against `photutils`, the standard photometry library.
"""
from __future__ import annotations

import argparse

import numpy as np


def _aperture_mask(shape, x, y, r):
    """Boolean mask of pixels whose *center* lies within radius r of (x, y).

    Strict `<` matches photutils' method='center' convention (a pixel exactly on
    the aperture edge is excluded), so our hand-rolled sum agrees with it exactly.
    """
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    return (xx - x) ** 2 + (yy - y) ** 2 < r ** 2


def aperture_flux(image, x, y, r=5.0, r_in=8.0, r_out=12.0):
    """Background-subtracted counts in a circular aperture at (x, y).

    Sky level is the median of the pixels in the annulus [r_in, r_out], which is
    robust to the odd contaminating star. Net = sum(aperture) − sky·N_aperture.
    """
    image = np.asarray(image, float)
    ap = _aperture_mask(image.shape, x, y, r)
    yy, xx = np.mgrid[0:image.shape[0], 0:image.shape[1]]
    rr2 = (xx - x) ** 2 + (yy - y) ** 2
    ann = (rr2 > r_in ** 2) & (rr2 <= r_out ** 2)
    sky = np.median(image[ann])
    return float(image[ap].sum() - sky * ap.sum())


def aperture_flux_raw(image, x, y, r=5.0):
    """Raw (no sky subtraction) aperture sum — used for the photutils cross-check."""
    image = np.asarray(image, float)
    return float(image[_aperture_mask(image.shape, x, y, r)].sum())


def instrumental_mag(flux, zeropoint=25.0):
    """Instrumental magnitude from net counts: m = ZP − 2.5 log₁₀(flux)."""
    return zeropoint - 2.5 * np.log10(np.asarray(flux, float))


def measure(image, positions, r=5.0, r_in=8.0, r_out=12.0, zeropoint=25.0):
    """Photometer a list of (x, y) positions; return dict of arrays."""
    flux = np.array([aperture_flux(image, x, y, r, r_in, r_out) for x, y in positions])
    return dict(flux=flux, mag=instrumental_mag(flux, zeropoint),
                x=np.array([p[0] for p in positions]),
                y=np.array([p[1] for p in positions]))


def _main() -> None:
    from astropy.io import fits
    from photutils.detection import DAOStarFinder
    from astropy.stats import sigma_clipped_stats

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--image", required=True, help="FITS image")
    p.add_argument("--r", type=float, default=5.0, help="aperture radius [pix]")
    p.add_argument("--nbright", type=int, default=10, help="report N brightest stars")
    args = p.parse_args()

    data = fits.getdata(args.image).astype(float)
    _, med, std = sigma_clipped_stats(data, sigma=3.0)
    found = DAOStarFinder(fwhm=4.0, threshold=15 * std)(data - med)
    pos = list(zip(found["x_centroid"], found["y_centroid"]))
    res = measure(data, pos, r=args.r)
    order = np.argsort(res["mag"])[:args.nbright]
    print(f"{'x':>7} {'y':>7} {'flux':>12} {'inst.mag':>9}")
    for i in order:
        print(f"{res['x'][i]:7.1f} {res['y'][i]:7.1f} {res['flux'][i]:12.1f} {res['mag'][i]:9.3f}")


if __name__ == "__main__":
    _main()
