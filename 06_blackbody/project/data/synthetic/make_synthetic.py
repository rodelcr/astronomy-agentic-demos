"""Generate a synthetic blackbody spectrum with a KNOWN temperature.

A Planck curve at a chosen temperature, sampled at the same frequencies as the real
FIRAS data, plus measurement noise. Seeded, with the true temperature in params.json,
so the test checks we recover it.

    python make_synthetic.py     # writes spectrum.csv + params.json here
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))      # project root, for scripts/
from scripts.blackbody import planck_MJy

TRUTH = dict(
    temperature=2.725,          # K — the answer key
    noise_frac=0.01,            # 1% of peak
    seed=9,
    freqs_icm=list(np.round(np.linspace(2.0, 21.0, 43), 3)),
)


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    freq = np.array(t["freqs_icm"])
    intensity = planck_MJy(freq, t["temperature"])
    noise = t["noise_frac"] * intensity.max()
    obs = intensity + rng.normal(0.0, noise, freq.size)
    unc = np.full(freq.size, noise)

    out = np.column_stack([freq, obs, unc])
    np.savetxt(HERE / "spectrum.csv", out, delimiter=",",
               header="freq_icm,intensity_MJy_sr,uncertainty_MJy_sr", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {freq.size}-point blackbody at T = {t['temperature']} K")


if __name__ == "__main__":
    main()
