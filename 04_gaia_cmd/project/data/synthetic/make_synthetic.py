"""Generate a synthetic cluster with a KNOWN distance and noisy parallaxes.

All stars sit at the same true distance, so the true parallax is identical; Gaia-like
measurement noise scatters the observed parallaxes. This is exactly the regime where
naively averaging 1/ϖ is biased — the test checks that our parallax-first estimator
recovers the injected distance.

    python make_synthetic.py     # writes cluster.csv + params.json here
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

TRUTH = dict(
    distance_pc=135.0,           # the answer key
    n_stars=500,
    parallax_error=0.08,         # mas, typical Gaia bright-star precision
    seed=3,
)


def main():
    t = TRUTH
    rng = np.random.default_rng(t["seed"])
    true_plx = 1000.0 / t["distance_pc"]
    err = np.full(t["n_stars"], t["parallax_error"])
    obs_plx = true_plx + rng.normal(0.0, t["parallax_error"], t["n_stars"])

    out = np.column_stack([obs_plx, err])
    np.savetxt(HERE / "cluster.csv", out, delimiter=",",
               header="parallax,parallax_error", comments="")
    (HERE / "params.json").write_text(json.dumps(t, indent=2))
    print(f"wrote {t['n_stars']} stars at {t['distance_pc']} pc "
          f"(true parallax {true_plx:.3f} mas)")


if __name__ == "__main__":
    main()
