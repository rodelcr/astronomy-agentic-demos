# Prompt walkthrough — solar-system orrery

Arc: **tests first → data straight from JPL → positions → physics → inspect → go live → notes.**
Paste these into Claude Code one at a time, in your own empty `08_solar_system/project/`.

### Step 0 — Orient
```
Read 08_solar_system/PLAN.md and project/README.md. What are we computing, what frame, and
what do we validate positions against vs. what is the independent physics check? No code.
```
**Look for:** Horizons checks our *usage*; Kepler III is the independent *physics* oracle.

### Step 1 — Tests first (red)
```
Write tests/test_ephemeris.py + a stub scripts/ephemeris.py so they fail:
  1. test_matches_horizons — heliocentric_ecliptic(body, t) matches cached JPL Horizons
     geometric vectors (< 1e-3 AU) at fixed TDB epochs.
  2. test_recovers_orbital_periods / test_kepler_third_law — orbital_period/semi_major_axis
     recover Earth/Mars/Jupiter/Saturn periods and P^2 ∝ a^3.
Run pytest, show red. Commit.
```
**Look for:** the Horizons test stores epochs as **TDB JD** so time-scales can't drift.

### Step 2 — Data straight from JPL
```
Write scripts/fetch_kernel.py: download de440s.bsp DIRECTLY from JPL NAIF (curl -C resume +
size check) into data/kernels/, and cache geometric heliocentric-ecliptic vectors from JPL
Horizons (astroquery.jplhorizons, location='@sun', refplane='ecliptic') into
data/reference/horizons_positions.csv. Run it. Commit the kernel + CSV.
```
**Look for:** bare ids `4`/`5` resolve to *barycenters* (not asteroids); Earth uses `399`.

### Step 3 — Positions (green)
```
Implement heliocentric_ecliptic: (body − Sun) from Skyfield (geometric, ICRF), then rotate
ICRF→J2000 ecliptic. Make test_matches_horizons pass. Add a --date CLI that prints each
planet's heliocentric distance + ecliptic longitude.
```
**Look for:** Skyfield's `ecliptic_frame` is the equinox *of date* — its error vs Horizons
**grows with epoch** (see TRANSCRIPT). The fixed **J2000** ecliptic (by-hand obliquity
rotation ε = 84381.448″, or `ecliptic_J2000_frame`) matches Horizons to ~1e-10 AU.

### Step 4 — Physics (green)
```
Implement orbital_period (watch ecliptic longitude advance by 2π) and semi_major_axis
((r_min+r_max)/2 over one orbit). Make the period + Kepler-III tests pass. Print P, a, P^2/a^3.
```
**Look for:** P²/a³ ≈ 1 for all eight planets — Kepler's third law, recovered from the kernel.

### Step 5 — Inspect
```
Write scripts/make_figures.py → results/orrery.png (top-down ecliptic, orbit traces) and
results/kepler_third_law.png (P² vs a³). LOOK: are the orbits concentric, ordered, closed?
```
**Look for:** a tilted or scattered orbit set is the ICRF→ecliptic frame bug.

### Step 6 — Go live
```
Write scripts/orrery.py — a Streamlit viewer with a date scrubber + a play button (rerun
loop), orbit traces, and a distance/longitude table. Keep draw_orrery() import-safe (no st
calls) so gui/app.py can reuse it. Then add panel_orrery to gui/app.py as the 8th panel.
```
**Look for:** inner planets visibly orbit faster than outer ones when you press play.

### Step 7 — Notes
```
Write notes/NOTES_orrery.md (frame/centre/light-time decisions, the ecliptic_frame gotcha,
data source, recovered numbers) and notes/HANDOFF_orrery.md. Update the root README table.
```

---
`git tag` lists `08-solar-step-1 … -step-7`.
