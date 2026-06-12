# Annotated transcript — solar-system orrery

A real slice of building this demo, centered on the frame-convention bug that actually
happened at step 3 — the ICRF→ecliptic rotation the PLAN flagged as the likely "wrong turn".

---

🧑 **You:** *(step 3)* "Implement `heliocentric_ecliptic`: subtract the Sun, then rotate into
the J2000 ecliptic. Make `test_matches_horizons` pass."

🤖 **Claude:** Reached for Skyfield's built-in ecliptic frame:
```python
from skyfield.framelib import ecliptic_frame
xyz = (eph[nid] - eph[10]).at(t).frame_xyz(ecliptic_frame).au
```
The test tolerance is 1e-3 AU and it **passes**. Ship it?

🧑 **You:** "It passes, but check the actual residual against Horizons at *several* epochs, not
just one. Same ephemeris on both sides should agree to ~1e-10 AU."

> ⚠️ **The wrong turn.** A *passing* test hiding a residual you can't explain is the trap.
> Skyfield and Horizons both ride DE440 — geometric positions should match to machine precision.

🤖 **Claude:** Tabulated jupiter's residual by epoch:
```
jd 2451544.5 (2000)  |Δ| = 3.4e-04 AU
jd 2455362.5 (2010)  |Δ| = 1.3e-02 AU
jd 2461203.5 (2026)  |Δ| = 3.4e-02 AU
```
It **grows with time from J2000** — that's the signature of **precession**, not light-time
(forcing Horizons `aberrations='geometric'` didn't help). Checked Skyfield's docstring:
`ecliptic_frame` is *"the true ecliptic and equinox **of date**."* But Horizons
`refplane='ecliptic'` is the **mean equinox of J2000** — a *fixed* reference epoch. The two
drift apart at the precession rate (~50″/yr).

🧑 **You:** "Right — use the fixed J2000 ecliptic. Do the obliquity rotation by hand so the
geometry is visible, and confirm it against `ecliptic_J2000_frame`."

🤖 **Claude:**
```python
EPS = radians(84381.448 / 3600)          # IAU76 obliquity at J2000 (fixed)
Rx = [[1,0,0],[0,cosE,sinE],[0,-sinE,cosE]]
xyz_ecl = Rx @ xyz_equatorial
```
```
by-hand J2000 rotation     : max |Δ| = 7.6e-11 AU   (all epochs)
ecliptic_J2000_frame       : max |Δ| = 7.6e-11 AU   (confirms it)
ecliptic_frame (of date)   : max |Δ| = 6.1e-02 AU   (the bug)
```
Both fixed-J2000 paths match Horizons to machine precision. We keep the by-hand rotation in
`ephemeris.py` — it makes the ~23.4° tilt explicit and is the teaching point.

### Takeaways
1. A **passing test with an unexplained residual** is a smell, not a success — and checking it
   at **several epochs** turned a vague "~1e-4 AU" into a clear *grows-with-time* signature.
2. **Epoch-dependent** error ⇒ precession ⇒ an *equinox-of-date vs J2000* frame mix-up. The
   classification came from the *pattern*, not a guess (it was not light-time).
3. The **absolute** cross-check against an independent service (Horizons) at multiple epochs is
   what made the frame bug visible — a shape-only or single-epoch check would have buried it.
   (Same lesson as demo 06's units bug and demo 07's pixel-window bias.)
