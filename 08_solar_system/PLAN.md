# Plan — Solar system from NASA ephemerides (live visualization)

> Design doc only — **not built yet**. This is the plan-mode artifact for a prospective
> 8th demo, written to the same conventions as `01`–`07`. It describes a *live demo
> program*: an interactive, time-controllable visualization of the solar system driven by
> JPL's definitive planetary ephemerides, with the positions validated against JPL Horizons.

## Context

NASA/JPL publishes the authoritative planetary ephemerides — the **DE series** (e.g.
DE440) — the same tables that fly spacecraft. A student loads them, computes where every
planet is at any instant, and builds a visualization they can scrub through time and play
like an orrery. The science is classic (Kepler's laws, ecliptic geometry); the point is the
agentic-coding craft: driving an ephemeris library, **validating positions against an
independent NASA service**, and turning a computation into an interactive, inspectable
visualization. It teaches the same five habits, and adds a genuinely *live* artifact.

## The science (what we compute & show)

- **Input data:** a bundled JPL ephemeris kernel (Skyfield's `de440s.bsp`, 1849–2150,
  ~32 MB — or `de421.bsp`, ~17 MB, if size matters). Heliocentric positions of the 8 planets
  (+ optionally Pluto, the Moon) at arbitrary times, in the J2000 ecliptic frame.
- **Method:** for a given time *t*, query the kernel for each body's barycentric position,
  subtract the Sun to get heliocentric vectors, rotate ICRF → ecliptic, project to the x–y
  plane for the top-down view (keep z for 3D). Sweep *t* to animate.
- **Headline artifacts:**
  - a **live interactive viewer** — a date/time slider + play button; planets orbit the Sun
    on the ecliptic, with orbit traces, heliocentric-distance and ecliptic-longitude readouts;
  - a **Kepler's-third-law** result recovered straight from the ephemeris (P² ∝ a³), the
    quantitative "did we get the physics right" check.
- **External answer key:** **JPL Horizons** (`astroquery.jplhorizons`) — an independent NASA
  ephemeris service. Skyfield positions must agree with Horizons at sample epochs.

## Approach (and the alternatives considered)

- **Chosen:** **Skyfield** for the ephemeris (clean time/position API, loads JPL BSP kernels
  directly, light-time and frame handling built in) + a **Streamlit** live viewer (consistent
  with this repo's GUI; a time slider and a "play" loop), with a matplotlib top-down plot and an
  optional 3D view. Validate against Horizons.
- **Rejected — astropy `get_body_barycentric` only:** works, but Skyfield's API for *time series*
  and frames is cleaner for an animation and for teaching the light-time/frame subtleties.
- **Rejected — raw SPICE (`spiceypy`):** most powerful and what JPL uses, but kernel-management
  overhead and a steeper API would bury the lesson. Note it as the "go deeper" path.
- **Rejected — a pre-baked movie:** the whole point is *live* and scrubbable; a static mp4 loses
  the interactivity that makes it a demo.

## Components (proposed layout — mirrors the other demos)

```
08_solar_system/
  PLAN.md                       (this file)
  project/
    README.md                   problem + a short ecliptic-geometry / Kepler scaffold
    notebook.ipynb              load kernel → positions → validate vs Horizons → Kepler's law → plot
    scripts/ephemeris.py        planet_position(t), heliocentric_ecliptic(t), orbital_period(body),
                                semi_major_axis(body) — importable + CLI (print a date's config)
    scripts/orrery.py           the live Streamlit viewer (time slider + play; 2D ecliptic, opt 3D)
    scripts/make_figures.py     static orrery snapshot + the P²–a³ Kepler plot
    tests/test_ephemeris.py     (a) positions match JPL Horizons; (b) recover known orbital
                                periods / Kepler's third law from the ephemeris
    data/
      kernels/de440s.bsp        bundled JPL kernel (public domain) — or a fetch script if too big
      reference/horizons_*.csv  cached Horizons positions at fixed epochs (offline test oracle)
    results/                    orrery.png, kepler_third_law.png
    notes/                      NOTES (frame/light-time/units decisions) + HANDOFF
    requirements.txt            skyfield, astroquery, numpy, matplotlib, astropy, pytest, streamlit
  walkthrough/
    PROMPTS.md                  numbered build spine (below)
    TRANSCRIPT.md               one annotated session incl. the likely "wrong turn" (frame/units)
    CHECKPOINTS.md              git-tag map
```

New env additions: **skyfield** (conda-forge). `astroquery`, `astropy`, `streamlit`, `matplotlib`
are already in the `demos` env.

## The `PROMPTS.md` spine (same shape as the other demos)

1. **Tests first (red):** `tests/test_ephemeris.py` asserting (a) a planet's heliocentric position
   at a fixed epoch matches a cached JPL Horizons value within tolerance, and (b) the recovered
   orbital period of Earth ≈ 365.25 d. Stub `ephemeris.py`. Run pytest → red.
2. **Get the data:** bundle the `de440s.bsp` kernel (or a fetch script); cache Horizons reference
   positions for a few planets/epochs to `data/reference/` so the test is deterministic & offline.
3. **Implement positions (green):** `planet_position(t)`, `heliocentric_ecliptic(t)` (subtract the
   Sun, rotate ICRF→ecliptic). Make the Horizons-match test pass. Add a CLI that prints a given
   date's planetary configuration.
4. **Recover the physics:** `orbital_period` (track ecliptic longitude over time, find the 2π
   wrap) and `semi_major_axis` (½(r_min+r_max) over an orbit). Make the period/Kepler test pass;
   plot P² vs a³ — a straight line through the origin.
5. **Inspect:** `make_figures.py` → a top-down orrery snapshot + the Kepler plot. *Look*: are the
   orbits roughly circular, ordered, and co-planar? An orbit that's wildly elliptical or tilted is
   a frame/units bug.
6. **Go live:** `orrery.py` — a Streamlit viewer with a date slider and a play button; planets
   move, orbit traces draw, readouts update. Weave: it imports the tested `ephemeris.py`.
7. **Notes:** decisions (frame = J2000 ecliptic; heliocentric astrometric vs apparent; AU vs km;
   light-time on/off), the data source, and the recovered numbers.

Each step is a commit + an `08-solar-step-N` tag.

## Verification

- `pytest` green: Skyfield positions match cached **JPL Horizons** (< ~10⁻³ AU, allowing for
  light-time/frame convention differences) **and** recovered orbital periods match known values
  (Earth ≈ 365.25 d; Jupiter ≈ 11.86 yr) within ~1%.
- `python scripts/ephemeris.py --date 2026-06-12` prints a sensible configuration (Earth ~1 AU,
  outer planets ordered by distance).
- `streamlit run scripts/orrery.py` opens the live viewer; the slider moves the planets and the
  inner planets visibly orbit faster than the outer ones.
- `results/kepler_third_law.png` is a clean straight line (P² ∝ a³) recovered from the ephemeris.
- Runs **offline** for the viewer and tests (bundled kernel + cached Horizons CSV); only
  regenerating the Horizons cache needs network.

## Risks / decisions to surface (the honest list)

- **Frame & projection:** ICRF (equatorial) vs J2000 **ecliptic** — forgetting the ~23.4° rotation
  tilts every orbit. This is the demo's most likely "wrong turn"; the orrery figure exposes it
  instantly (orbits won't lie flat).
- **Heliocentric vs barycentric vs apparent:** subtract the **Sun** (not the solar-system
  barycenter) for a heliocentric orrery; decide astrometric (geometric) vs apparent (light-time +
  aberration) and state it. The Horizons query must use the *same* settings or the test will
  "disagree" for a convention reason, not a bug (cf. demo 07's lesson).
- **Units:** AU vs km vs ecliptic-longitude degrees — pick AU + degrees and convert at the edges.
- **Kernel size / licensing:** JPL kernels are public domain; `de440s.bsp` (~32 MB) is committable
  but large — a `fetch_kernel.py` (like demo 07's SMICA fetch) is the fallback, with the kernel
  gitignored.
- **"Live" performance:** recomputing all bodies every slider tick is fine (ephemeris lookups are
  fast), but cache positions per time-step (`st.cache_data`) so the play loop stays smooth.
- **Network for Horizons:** the live test uses a *cached* Horizons response so it's deterministic
  and offline; a separate, network-gated check can refresh the cache.

## Why this fits the collection

It adds the one modality the other seven lack — a **time-domain, interactive 3D visualization** —
while keeping every habit: a tested `ephemeris.py` validated against an independent NASA service
(Horizons), a recovered physics result (Kepler III) as the synthetic-truth oracle, an inspectable
figure that catches the frame bug, notes on the convention choices, and a genuinely *live* artifact
that's perfect for standing in front of a room.
