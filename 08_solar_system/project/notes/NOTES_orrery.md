# NOTES — solar-system orrery demo

## Decisions

- **Ephemeris:** JPL **DE440** short kernel (`de440s.bsp`, 1849–2150, ~31 MB), loaded with
  **Skyfield**. Fetched directly from NASA **NAIF** and committed so the demo runs offline.
- **Frame:** **J2000 ecliptic**, obtained by rotating the ICRF (equatorial) vector about x by
  the IAU76 obliquity **ε = 84381.448″ = 23.4392911°**. We do this rotation **by hand**, not
  with Skyfield's built-in `ecliptic_frame` — see the gotcha below.
- **Centre:** heliocentric — subtract the **Sun** (body 10), not the solar-system barycenter.
- **Aberration:** **geometric** (no light-time, no aberration) on both sides, so our positions
  match Horizons' geometric vectors to machine precision.
- **Body ids:** barycenters for Mars–Neptune (de440s ships no planet-centre segments for them);
  **Earth = 399** (the Earth centre, not the Earth–Moon barycenter, to avoid a ~monthly wobble).
- **No synthetic data.** Unlike demos 01–07 there is no `data/synthetic/` generator: the
  ephemeris *is* the data, and the "known answer" we recover is the **physics** (orbital periods,
  Kepler III), not an injected number.

## Gotcha / the wrong turn (frame definition)

First cut rotated to the ecliptic with Skyfield's `framelib.ecliptic_frame`. The test (1e-3 AU
tolerance) *passed*, but the residual against Horizons was suspicious and — crucially — **grew
with epoch**: jupiter was off by 3×10⁻⁴ AU at J2000, 1.3×10⁻² AU in 2010, 3.4×10⁻² AU in 2026.
A residual that grows with time from J2000 is **precession**. `ecliptic_frame` is the ecliptic
& equinox *of date*; Horizons `refplane='ecliptic'` is the **mean equinox of J2000** (the fixed
reference epoch). The fix: use the **fixed J2000 ecliptic** — either the textbook obliquity
rotation by hand (ε = 84381.448″, which we do, for transparency) or Skyfield's
`framelib.ecliptic_J2000_frame`. Both match Horizons to **~10⁻¹⁰ AU** at every epoch. (It was
*not* light-time: forcing Horizons `aberrations='geometric'` did not help.) Lesson (cf. demo 07):
a *passing* test with an unexplained, **epoch-dependent** residual is a convention bug, and the
absolute cross-check against an independent service is what exposes it.

## Independence caveat

Horizons and Skyfield both ride on the **same JPL DE ephemeris**. So the Horizons test checks
our **usage** (frame, centre, light-time), not the underlying model. The independent check is
the **physics** — Kepler's third law recovered from the positions.

## Data source

- Kernel: `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp`
  (NASA/JPL NAIF, public domain). Content-Length 32,726,016 bytes.
- Horizons oracle: `astroquery.jplhorizons`, `location='@sun'`, `refplane='ecliptic'`,
  `aberrations='geometric'`, at 2000-01-01 / 2010-06-15 / 2026-06-12 (TDB).

## Numbers (recovered from de440s)

| body | P (yr) | a (AU) | P²/a³ |
|------|--------|--------|-------|
| mercury | 0.241 | 0.387 | 1.000 |
| earth | 1.000 | 1.000 | 1.000 |
| jupiter | 11.860 | 5.203 | 0.999 |
| neptune | 164.79 | 30.07 | 0.999 |

- Skyfield ↔ Horizons geometric positions: agree to **< 10⁻³ AU** (actually ~10⁻¹⁰ AU).
- Orbital periods recovered within ~1% of literature; Kepler III holds across all eight planets.
