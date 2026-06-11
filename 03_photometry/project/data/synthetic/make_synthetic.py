"""Generate a synthetic star field with KNOWN fluxes and positions.

Each star is a 2-D Gaussian (the point-spread function) with a chosen total flux,
on a flat sky background plus Poisson-like noise. Because we know every star's true
flux, the test can check that measured magnitude *differences* match the truth — the
aperture loses the same fraction of every star's light (same PSF), so relative
photometry is exact even though absolute aperture flux is not.

    python make_synthetic.py     # writes starfield.npy + params.json here
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

TRUTH = dict(
    shape=[200, 200],
    fwhm=4.0,
    sky=100.0,
    noise=3.0,
    seed=11,
    # (x, y, total_flux) for each star — the answer key
    stars=[
        [40.0, 50.0, 50000.0],
        [120.0, 60.0, 20000.0],
        [150.0, 150.0, 80000.0],
        [60.0, 160.0, 12000.0],
        [100.0, 110.0, 32000.0],
    ],
)


def gaussian_psf(shape, x0, y0, flux, fwhm):
    sigma = fwhm / 2.3548
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    g = np.exp(-((xx - x0) ** 2 + (yy - y0) ** 2) / (2 * sigma ** 2))
    return flux * g / g.sum()          # normalized so the total equals `flux`


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    img = np.full(t["shape"], t["sky"], float)
    for x0, y0, flux in t["stars"]:
        img += gaussian_psf(t["shape"], x0, y0, flux, t["fwhm"])
    img += rng.normal(0.0, t["noise"], size=t["shape"])

    np.save(HERE / "starfield.npy", img.astype("float32"))
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {len(t['stars'])}-star field {t['shape']}")


if __name__ == "__main__":
    main()
