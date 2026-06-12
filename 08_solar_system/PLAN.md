# Plan — Solar system orrery from NASA/JPL ephemerides (live visualization)

> The design doc, written before code (your plan-mode output). `walkthrough/PROMPTS.md`
> executes this; `project/` is the result. This demo adds the one modality the other
> seven lack — a **time-domain, interactive visualization** — driven by JPL's definitive
> planetary ephemerides and validated against an independent NASA service.

## Context

NASA/JPL publishes the authoritative planetary ephemerides — the **DE series** (DE440) —
the same tables that fly spacecraft. A student loads them, computes where every planet is
at any instant, and builds a viewer they can scrub through time and play like an orrery.
The science is classic (Kepler's laws, ecliptic geometry); the point is the agentic-coding
craft: driving an ephemeris library, **validating positions against an independent NASA
service (JPL Horizons)**, recovering a physics result as the truth oracle, and turning a
computation into a *live, inspectable* visualization. It teaches the same five habits and
adds a genuinely live artifact.

## The science (what we compute & show)

- **Input data:** a JPL ephemeris kernel (`de440s.bsp`, 1849–2150, ~32 MB), fetched
  **directly from JPL NAIF** and committed so the demo runs offline. Heliocentric positions
  of the 8 planets in the **J2000 ecliptic** frame.
- **Method:** for a time *t*, look up each body's barycentric position from the kernel,
  subtract the Sun → heliocentric vector, rotate ICRF → J2000 ecliptic, project to the x–y
  plane for the top-down orrery (keep z for 3D). Sweep *t* to animate. **Geometric** positions
  (no light-time/aberration) on both sides so the comparison is clean.
- **Headline output (the truth oracle):** recover **Kepler's third law** (P² ∝ a³) and the
  known orbital periods (Earth ≈ 365.25 d, Jupiter ≈ 11.86 yr) straight from the ephemeris —
  the quantitative "did we get the physics right" check, independent of any library.
- **External answer key:** **JPL Horizons** (`astroquery.jplhorizons`) — an independent NASA
  ephemeris *service*. Skyfield positions must agree with Horizons at sample epochs.

> **Independence caveat (stated honestly).** Skyfield (`de440s`) and Horizons both derive
> from the **same JPL DE ephemeris family**. So the Horizons cross-check validates *our
> usage* — frame rotation, heliocentric subtraction, light-time convention — **not the
> ephemeris model itself**. The genuinely independent check is the *physics*: Kepler III
> recovered from the positions. (Cf. demo 02's "independence is the point.")

## Approach (and the alternatives rejected)

- **Chosen:** **Skyfield** for the ephemeris (clean time/position API, loads JPL BSP kernels
  directly, frame + light-time handling built in) + a **Streamlit** live viewer (consistent
  with this repo's GUI), delivered **two ways**: a standalone `scripts/orrery.py` (full
  play loop) and an 8th panel added to the unified `gui/app.py`. Validate against Horizons;
  recover Kepler III as the oracle.
- **Rejected — astropy `get_body_barycentric` only:** works, but Skyfield's time-series and
  frame API is cleaner for an animation and for teaching the light-time/frame subtleties.
- **Rejected — raw SPICE (`spiceypy`):** most powerful and what JPL uses, but kernel-management
  overhead and a steeper API bury the lesson. Noted as the "go deeper" path.
- **Rejected — a synthetic two-body generator:** the other demos inject a known answer into
  synthetic data; here the ephemeris *is* the data and the known answer is the *physics*
  (Kepler III / known periods). No `data/synthetic/` for this demo — a deliberate deviation.
- **Rejected — a pre-baked movie:** the whole point is *live* and scrubbable.

## Components

| File | Responsibility |
|------|----------------|
| `scripts/ephemeris.py` | `planet_position`, `heliocentric_ecliptic`, `orbital_period`, `semi_major_axis`; importable + CLI |
| `scripts/fetch_kernel.py` | download `de440s.bsp` **directly from JPL NAIF** (resume + size check); cache Horizons reference CSVs |
| `scripts/make_figures.py` | top-down orrery snapshot + the P²–a³ Kepler plot |
| `scripts/orrery.py` | the standalone live Streamlit viewer (scrubber + play; 2D ecliptic) |
| `tests/test_ephemeris.py` | (a) positions match cached JPL Horizons; (b) recover orbital periods / Kepler III |
| `data/kernels/de440s.bsp` | bundled JPL kernel (committed, ~32 MB) — offline by default |
| `data/reference/horizons_*.csv` | cached Horizons positions at fixed epochs (offline test oracle) |
| `notebook.ipynb` | load kernel → positions → validate vs Horizons → Kepler's law → plot |
| `results/` | `orrery.png`, `kepler_third_law.png` |
| `notes/` | NOTES (frame/light-time/units + independence caveat) + HANDOFF |
| `gui/app.py` (`panel_orrery`) | out-of-tree: the orrery as the dashboard's 8th panel |

New env addition: **skyfield** (conda-forge). `astroquery`, `astropy`, `streamlit`,
`matplotlib` are already in the `demos` env.

## Build steps

Steps 1–7 of `walkthrough/PROMPTS.md`, each a commit + `08-solar-step-N` tag:
failing Horizons/period tests → fetch kernel+oracle from JPL → positions green
(ICRF→ecliptic) → physics green (period + Kepler III) → inspect figures → go live
(standalone viewer + GUI panel) → notes + walkthrough.

## Verification

- `pytest` green: Skyfield positions match cached **JPL Horizons** (< ~10⁻³ AU) **and**
  recovered orbital periods match known values (Earth ≈ 365.25 d, Jupiter ≈ 11.86 yr) within
  ~1%, with P² ∝ a³ across the planets.
- `python scripts/ephemeris.py --date 2026-06-12` prints a sensible configuration (Earth
  ~1 AU, outer planets ordered by distance).
- `streamlit run scripts/orrery.py` opens the live viewer; the scrubber moves the planets,
  the play button auto-advances, inner planets visibly orbit faster than outer ones.
- `streamlit run gui/app.py` shows the 8th orrery panel.
- `results/kepler_third_law.png` is a clean straight line (P² ∝ a³); `results/orrery.png`
  shows flat, co-planar, ordered orbits.
- Runs **offline** for the viewer and tests (committed kernel + cached Horizons CSV); only
  regenerating the data with `fetch_kernel.py` needs network.

## Risks / decisions to surface (the honest list)

- **Frame & projection:** ICRF (equatorial) vs J2000 **ecliptic** — forgetting the ~23.4°
  rotation tilts every orbit. This is the demo's "wrong turn"; the orrery figure exposes it
  instantly (orbits won't lie flat). It is the centerpiece of `walkthrough/TRANSCRIPT.md`.
- **Heliocentric vs barycentric vs apparent:** subtract the **Sun** (not the SSB) for a
  heliocentric orrery; use **geometric** (no light-time/aberration) positions and make the
  Horizons query use the *same* setting, or the test "disagrees" for a convention reason, not
  a bug (cf. demo 07's lesson). Earth uses body 399 (not the Earth–Moon barycenter) to avoid a
  monthly wobble.
- **Units:** AU for distance, degrees for ecliptic longitude; convert at the edges.
- **Independence:** Skyfield and Horizons share the JPL ephemeris — Horizons checks our
  *usage*, Kepler III checks the *physics* (see caveat above). Don't overclaim independence.
- **Kernel size / licensing:** JPL kernels are public domain; `de440s.bsp` (~32 MB) is
  committed so the demo is offline-by-default; `fetch_kernel.py` regenerates it from NAIF.
- **"Live" performance:** recomputing all bodies per slider tick is fine (lookups are fast),
  but cache positions per time-step (`st.cache_data`) so the play loop stays smooth.

## Why this fits the collection

It adds the one modality the other seven lack — a **time-domain, interactive visualization** —
while keeping every habit: a tested `ephemeris.py` validated against an independent NASA
service (Horizons), a recovered physics result (Kepler III) as the truth oracle, an
inspectable figure that catches the frame bug, notes on the convention choices, and a
genuinely *live* artifact that's perfect for standing in front of a room.
