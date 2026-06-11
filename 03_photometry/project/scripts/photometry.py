"""photometry.py — aperture photometry on an image. STUB (step 1)."""
from __future__ import annotations


def aperture_flux(image, x, y, r=5.0, r_in=8.0, r_out=12.0):
    raise NotImplementedError("implemented at step 3")


def aperture_flux_raw(image, x, y, r=5.0):
    raise NotImplementedError("implemented at step 3")


def instrumental_mag(flux, zeropoint=25.0):
    raise NotImplementedError("implemented at step 3")


def measure(image, positions, r=5.0, r_in=8.0, r_out=12.0, zeropoint=25.0):
    raise NotImplementedError("implemented at step 3")
