# HANDOFF — solar-system orrery demo

**TL;DR.** Load JPL's DE440 ephemeris, compute heliocentric J2000-ecliptic planet positions,
and build a live, scrubbable orrery. Positions match the independent **JPL Horizons** service
to ~10⁻¹⁰ AU; orbital periods and **Kepler's third law** (P²/a³ = 1.000 ± 0.001) are recovered
straight from the ephemeris for all eight planets.

## What's here

| File | What it is |
|------|------------|
| `scripts/ephemeris.py` | `heliocentric_ecliptic`, `orbital_period`, `semi_major_axis`, `orbit_track` + CLI |
| `scripts/orrery.py` | live Streamlit viewer (scrubber + play); import-safe `draw_orrery` |
| `scripts/fetch_kernel.py` | fetch `de440s.bsp` from NAIF + cache the Horizons oracle |
| `scripts/make_figures.py` | `results/orrery.png`, `results/kepler_third_law.png` |
| `tests/test_ephemeris.py` | Horizons-match + period/Kepler-III recovery |
| `data/kernels/de440s.bsp` | bundled JPL ephemeris (committed, offline) |
| `data/reference/horizons_positions.csv` | cached Horizons vectors (test oracle) |
| `notebook.ipynb` | kernel → positions → Horizons check → Kepler → orrery |

## Reproduce

```bash
conda activate demos
python scripts/fetch_kernel.py          # only to regenerate the committed kernel + oracle (network)
pytest                                  # offline: Horizons match + Kepler III
python scripts/make_figures.py
python scripts/ephemeris.py --date 2026-06-12
streamlit run scripts/orrery.py         # the live orrery
streamlit run ../../gui/app.py          # the orrery as the dashboard's 8th panel
```

## Validation status

- ✅ Skyfield heliocentric-ecliptic positions match JPL Horizons geometric vectors (< 10⁻³ AU).
- ✅ Recovered orbital periods within ~1% (Earth 365.3 d, Jupiter 11.86 yr, Neptune 164.8 yr).
- ✅ Kepler's third law P²/a³ = 1.000 ± 0.001 across all eight planets.
- ✅ Runs offline (committed kernel + cached Horizons CSV); GUI panel + standalone viewer boot.

## Key insight / gotcha

The ICRF→ecliptic rotation must use the **fixed J2000** ecliptic (ε = 84381.448″ by hand, or
Skyfield's `ecliptic_J2000_frame`). Skyfield's `ecliptic_frame` is the equinox *of date* and
precesses away from Horizons' J2000 ecliptic — an **epoch-growing** residual (~0.06 AU by 2026)
that still slips under a loose tolerance. The absolute Horizons cross-check exposed it. See
`NOTES_orrery.md`.

## Outstanding / extensions

- Add Pluto / the Moon; a 3D (x–z) view to *show* co-planarity directly.
- Apparent (light-time + aberration) positions as a toggle, vs the geometric default.
- Inner-planet conjunctions / oppositions readout; an "on this date" ephemeris export.
- Go deeper with raw SPICE (`spiceypy`) and a full DE440 (not the short kernel).
