"""orrery.py — a live, scrubbable solar-system viewer driven by the JPL ephemeris.

    conda activate demos
    streamlit run scripts/orrery.py

Drag the date to scrub the planets through time, or hit play to let it run. Every position is
the SAME tested `scripts/ephemeris.py` function the test-suite validates against JPL Horizons —
no separate, untrusted visualization code. Runs fully offline on the bundled de440s kernel.

`draw_orrery()` and `positions_table()` are import-safe (no Streamlit calls), so the unified
dashboard (`gui/app.py`) reuses them; the Streamlit UI lives under `if __name__ == '__main__'`.
"""
from __future__ import annotations

import datetime as dt
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from scripts.ephemeris import heliocentric_ecliptic, orbit_track, PLANETS, _load  # noqa: E402

COLORS = {"mercury": "#8c8c8c", "venus": "#d9a066", "earth": "#3b7dd8", "mars": "#c1440e",
          "jupiter": "#d8a25e", "saturn": "#e3c777", "uranus": "#8fd6e1", "neptune": "#4b6fd6"}
VIEWS = {"inner (Mercury–Mars)": (PLANETS[:4], 1.8), "all eight planets": (PLANETS, 31.0)}
MIN_DATE, MAX_DATE = dt.date(1850, 1, 1), dt.date(2149, 12, 31)   # de440s coverage

_TRACKS: dict[str, np.ndarray] = {}


def _track(body):
    """Cache one-orbit traces (they don't depend on the chosen date)."""
    if body not in _TRACKS:
        _TRACKS[body] = orbit_track(body, 500)
    return _TRACKS[body]


def _time(cur):
    ts, _ = _load()
    return ts.utc(cur.year, cur.month, cur.day)


def positions_table(cur):
    """List of (body, r_AU, ecliptic_longitude_deg) at date `cur`."""
    t = _time(cur)
    rows = []
    for b in PLANETS:
        x, y, z = heliocentric_ecliptic(b, t)
        rows.append((b, float(np.sqrt(x * x + y * y + z * z)),
                     float(np.degrees(np.arctan2(y, x))) % 360.0))
    return rows


def draw_orrery(cur, view="all eight planets"):
    """Top-down J2000-ecliptic snapshot at date `cur`. Returns a matplotlib figure."""
    bodies, lim = VIEWS[view]
    t = _time(cur)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(0, 0, "o", color="gold", ms=16, zorder=5)
    for b in bodies:
        xyz = _track(b)
        ax.plot(xyz[0], xyz[1], "-", lw=0.8, color=COLORS[b], alpha=0.5)
        x, y, _ = heliocentric_ecliptic(b, t)
        ax.plot(x, y, "o", color=COLORS[b], ms=8, zorder=4)
        ax.annotate(b, (x, y), textcoords="offset points", xytext=(6, 5), fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xlabel("x (AU)"); ax.set_ylabel("y (AU)")
    ax.set_title(f"{cur:%Y-%m-%d}  ·  heliocentric J2000 ecliptic")
    fig.tight_layout()
    return fig


def main():
    import streamlit as st
    st.set_page_config(page_title="Orrery", layout="centered")
    st.title("🪐 Live orrery — JPL ephemeris")
    st.caption("Drag the date to scrub time, or press play. Positions come straight from the "
               "tested `ephemeris.py` (validated against JPL Horizons). Offline, on de440s.")

    view = st.sidebar.radio("view", list(VIEWS))
    speed = st.sidebar.slider("days per frame", 1, 120, 20)
    fps = st.sidebar.slider("frames / sec", 2, 20, 10)
    if "cur" not in st.session_state:
        st.session_state.cur = dt.date(2026, 6, 12)
    if "playing" not in st.session_state:
        st.session_state.playing = False

    c1, c2, c3 = st.columns(3)
    if c1.button("▶ play"):
        st.session_state.playing = True
    if c2.button("⏸ pause"):
        st.session_state.playing = False
    if c3.button("⟲ reset"):
        st.session_state.cur = dt.date(2026, 6, 12); st.session_state.playing = False

    cur = st.slider("date", MIN_DATE, MAX_DATE, st.session_state.cur,
                    step=dt.timedelta(days=1), format="YYYY-MM-DD")
    st.session_state.cur = cur

    st.pyplot(draw_orrery(cur, view))

    rows = positions_table(cur)
    st.dataframe({"body": [r[0] for r in rows],
                  "r (AU)": [round(r[1], 3) for r in rows],
                  "ecl. lon (°)": [round(r[2], 1) for r in rows]},
                 hide_index=True, use_container_width=True)

    if st.session_state.playing:
        nxt = cur + dt.timedelta(days=speed)
        st.session_state.cur = MIN_DATE if nxt > MAX_DATE else nxt
        time.sleep(1.0 / fps)
        st.rerun()


if __name__ == "__main__":
    main()
