# Checkpoint tags — solar-system orrery

| Tag | Captures |
|-----|----------|
| `08-solar-step-1` | failing tests (Horizons match + Kepler III) against a stub `ephemeris.py` |
| `08-solar-step-2` | `fetch_kernel.py`; committed `de440s.bsp` (from NAIF) + Horizons oracle CSV |
| `08-solar-step-3` | `heliocentric_ecliptic` (by-hand ICRF→ecliptic); **Horizons test green** + `--date` CLI |
| `08-solar-step-4` | `orbital_period` + `semi_major_axis`; **Kepler-III test green** (P²/a³ ≈ 1) |
| `08-solar-step-5` | `make_figures.py` + `results/` orrery & Kepler plots; `orbit_track` helper |
| `08-solar-step-6` | `orrery.py` live viewer (scrubber + play) + `panel_orrery` in `gui/app.py` |
| `08-solar-step-7` | `notebook.ipynb`, `notes/` NOTES + HANDOFF, walkthrough, README updates |

```bash
git checkout 08-solar-step-3      # right after positions matched Horizons
git diff   08-solar-step-3 -- 08_solar_system/project/scripts/ephemeris.py
```
