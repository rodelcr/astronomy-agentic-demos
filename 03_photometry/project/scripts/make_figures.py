"""Render the inspection figures for the photometry demo.

    python scripts/make_figures.py     # writes results/apertures.png, results/compare.png

The apertures figure is the inspection that matters: are the circles actually centered
on stars, and are the sky annuli free of bright neighbors? The compare figure shows our
hand-rolled aperture sums against photutils — they should fall on the 1:1 line.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.visualization import simple_norm
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, aperture_photometry

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.photometry import aperture_flux_raw  # noqa: E402

R, R_IN, R_OUT = 6.0, 10.0, 15.0


def main():
    data = fits.getdata(PROJECT / "data" / "real" / "m67_cutout.fits").astype(float)
    _, med, std = sigma_clipped_stats(data, sigma=3.0)
    found = DAOStarFinder(fwhm=4.0, threshold=20 * std)(data - med)
    found.sort("flux")
    found.reverse()
    bright = found[:15]
    pos = list(zip(bright["x_centroid"], bright["y_centroid"]))

    # --- figure 1: apertures on the image ---
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(data, origin="lower", cmap="gray",
              norm=simple_norm(data, "sqrt", percent=99.5))
    for x, y in pos:
        ax.add_patch(Circle((x, y), R, ec="cyan", fc="none", lw=1.2))
        ax.add_patch(Circle((x, y), R_IN, ec="yellow", fc="none", lw=0.5, ls=":"))
        ax.add_patch(Circle((x, y), R_OUT, ec="yellow", fc="none", lw=0.5, ls=":"))
    ax.set_title("M67 cutout — 15 brightest stars\n(cyan aperture, yellow sky annulus)")
    ax.set_xlabel("x [pix]"); ax.set_ylabel("y [pix]")
    fig.savefig(PROJECT / "results" / "apertures.png", dpi=130, bbox_inches="tight")

    # --- figure 2: ours vs photutils ---
    ours = np.array([aperture_flux_raw(data, x, y, R) for x, y in pos])
    ref = aperture_photometry(data, CircularAperture(pos, r=R),
                              method="center")["aperture_sum"].data
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.plot(ref, ours, "o", color="crimson")
    lims = [min(ref.min(), ours.min()), max(ref.max(), ours.max())]
    ax2.plot(lims, lims, "-", color="0.5", lw=1, label="1:1")
    ax2.set_xlabel("photutils aperture sum"); ax2.set_ylabel("our aperture sum")
    ax2.set_title("hand-rolled vs photutils (raw aperture)")
    ax2.legend()
    fig2.savefig(PROJECT / "results" / "compare.png", dpi=130, bbox_inches="tight")

    maxdiff = np.max(np.abs(ours - ref) / ref)
    print(f"{len(pos)} stars; max fractional diff vs photutils = {maxdiff:.2e}")


if __name__ == "__main__":
    main()
