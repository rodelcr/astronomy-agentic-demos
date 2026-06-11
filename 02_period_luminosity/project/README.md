# Period of a Cepheid — the distance ladder's first rung

## The problem

Some stars pulsate, brightening and dimming on a regular cycle. For **Cepheids**,
the pulsation *period* predicts the *luminosity* (the period–luminosity, or Leavitt,
law), so measuring the period gives the distance. Here we measure the period of
**V1154 Cyg**, the only classical Cepheid in the Kepler field.

## Physics scaffold

The light curve repeats every period P. To find P we **fold**: try a period, wrap
the times onto phase = (t / P) mod 1, and see whether the points line up into one
clean cycle. We score "line up" with the **string length** — the total length of the
line joining phase-sorted points. The right period minimizes it.

Once P is known, the **Leavitt law** gives the absolute magnitude,
M_V ≈ −2.43 (log₁₀P − 1) − 4.05, and with the apparent magnitude the distance follows
from the distance modulus μ = V − M_V.

> Headline result: **P = 4.925 d** for V1154 Cyg (literature 4.9254 d), recovered by
> two independent methods to 0.3%.

## What's in here

```
project/
  notebook.ipynb        explore → period (string-length + Lomb-Scargle) → fold → distance
  scripts/variable.py   string_length_period, phase_fold, lombscargle_period — importable + CLI
  tests/test_variable.py  recover injected period + agree with Lomb-Scargle
  data/
    real/v1154cyg_q3.csv    real Kepler V1154 Cyg quarter (time_bkjd, mag, mag_err)
    synthetic/              make_synthetic.py + params.json ground truth
  results/              periodogram.png, folded.png
  notes/                NOTES + HANDOFF
  requirements.txt
```

## Run it

```bash
conda activate demos
pytest
python scripts/variable.py --data data/real/v1154cyg_q3.csv --pmin 3 --pmax 7
```

## External answer key

Our **string-length** period is validated against **`astropy.timeseries.LombScargle`**
— a Fourier-based, architecturally independent method. See
`tests/test_variable.py::test_agrees_with_lombscargle`.

## Data provenance

`data/real/v1154cyg_q3.csv` is **real** Kepler SAP photometry of KIC 7548061
(V1154 Cyg), downloaded from MAST and converted to relative magnitudes. Nothing
here is fabricated. The Leavitt-law distance step uses a literature calibration and
apparent magnitude and is labeled as a scaffolded illustration in the notebook.
