"""Astronomy demos — interactive dashboard.

A Streamlit app that turns the six demos into live, slider-driven visualizations:
drag a parameter and watch the fit respond. It reuses the SAME functions the demos
test (`scripts/*.py` in each demo), so what you see here is exactly what the tests
verify — no separate, untrusted visualization code.

Run it:

    conda activate demos
    streamlit run gui/app.py

Everything is offline (bundled data). No network, no API, no live model needed.
"""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import streamlit as st

REPO = Path(__file__).resolve().parent.parent


# --- load each demo's estimator module by file path (no package collisions) ---------
def _load(demo_dir, module):
    path = REPO / demo_dir / "project" / "scripts" / f"{module}.py"
    spec = importlib.util.spec_from_file_location(f"{demo_dir}_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@st.cache_resource
def estimators():
    return dict(
        transit=_load("01_transit", "transit"),
        variable=_load("02_period_luminosity", "variable"),
        photometry=_load("03_photometry", "photometry"),
        cluster=_load("04_gaia_cmd", "cluster"),
        hubble=_load("05_hubble", "hubble"),
        blackbody=_load("06_blackbody", "blackbody"),
    )


@st.cache_data
def load_csv(demo_dir, name):
    p = REPO / demo_dir / "project" / "data" / "real" / name
    return np.loadtxt(p, delimiter=",", skiprows=1)


# =====================================================================================
# Demo panels — each returns a matplotlib figure + a short caption
# =====================================================================================
def panel_transit(E):
    st.subheader("Exoplanet transit — Kepler-8 b")
    st.caption("Drag the period off its true value and watch the folded transit smear away.")
    arr = load_csv("01_transit", "kepler8_q3.csv")
    t, f, fe = arr[:, 0], arr[:, 1], arr[:, 2]
    period = st.slider("trial period (days)", 3.40, 3.65, 3.52254, 0.0005, format="%.5f")
    t0 = st.slider("epoch t0 (BKJD)", 169.0, 172.0, 170.4408, 0.01)
    res = E["transit"].fit_transit(t, f, fe, period=period, t0=t0, window=0.06)
    ph = E["transit"].phase_fold(t, period, t0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ph, f, ".", ms=2, color="0.6")
    ax.plot(res["phase"], res["model"], "-", color="crimson", lw=2)
    ax.set_xlim(-0.06, 0.06); ax.set_xlabel("phase"); ax.set_ylabel("flux")
    st.pyplot(fig)
    st.metric("recovered Rp/R*", f"{res['rp_over_rstar']:.4f}", help="literature 0.0944")


def panel_period(E):
    st.subheader("Cepheid period — V1154 Cyg")
    st.caption("Slide the trial period; only the true period folds the light curve into one clean cycle.")
    arr = load_csv("02_period_luminosity", "v1154cyg_q3.csv")
    t, m = arr[:, 0], arr[:, 1]
    period = st.slider("trial period (days)", 2.0, 7.0, 4.9252, 0.0005, format="%.4f")
    ph = E["variable"].phase_fold(t, period)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.r_[ph, ph + 1], np.r_[m, m], ".", ms=2, color="0.4")
    ax.invert_yaxis(); ax.set_xlabel("phase"); ax.set_ylabel("rel. mag")
    st.pyplot(fig)
    if st.checkbox("show the string-length periodogram (find the minimum)"):
        P_sl, per, ln = E["variable"].string_length_period(t, m, 3.0, 7.0, n_periods=3000)
        fig2, ax2 = plt.subplots(figsize=(7, 2.6))
        ax2.plot(per, ln, "-", color="0.4"); ax2.axvline(period, color="crimson")
        ax2.set_xlabel("trial period"); ax2.set_ylabel("string length")
        st.pyplot(fig2)
        st.metric("best period (string length)", f"{P_sl:.4f} d", help="literature 4.9254 d")


def panel_photometry(E):
    st.subheader("Aperture photometry — M67")
    st.caption("Resize the aperture and sky annulus and watch the measured flux change.")
    from astropy.io import fits
    from astropy.visualization import simple_norm
    data = fits.getdata(REPO / "03_photometry/project/data/real/m67_cutout.fits").astype(float)
    r = st.slider("aperture radius (pix)", 2.0, 12.0, 6.0, 0.5)
    r_in, r_out = st.slider("sky annulus (pix)", 2.0, 25.0, (10.0, 15.0))
    # one bright, well-separated star near the center
    x, y = 341.7, 152.6
    flux = E["photometry"].aperture_flux(data, x, y, r, r_in, r_out)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.imshow(data, origin="lower", cmap="gray", norm=simple_norm(data, "sqrt", percent=99.5))
    ax.add_patch(Circle((x, y), r, ec="cyan", fc="none", lw=1.5))
    ax.add_patch(Circle((x, y), r_in, ec="yellow", fc="none", lw=0.8, ls=":"))
    ax.add_patch(Circle((x, y), r_out, ec="yellow", fc="none", lw=0.8, ls=":"))
    ax.set_xlim(x - 30, x + 30); ax.set_ylim(y - 30, y + 30)
    st.pyplot(fig)
    st.metric("net flux / inst. mag",
              f"{flux:.0f} / {float(E['photometry'].instrumental_mag(flux)):.3f}")


def panel_cmd(E):
    st.subheader("Color–magnitude diagram — Pleiades")
    st.caption("Tighten the parallax-error cut to clean field stars off the main sequence.")
    rows = list(csv.DictReader(open(REPO / "04_gaia_cmd/project/data/real/pleiades_gaia.csv")))
    plx = np.array([float(r["parallax"]) for r in rows])
    err = np.array([float(r["parallax_error"]) for r in rows])
    g = np.array([float(r["phot_g_mean_mag"]) for r in rows])
    bp_rp = np.array([float(r["bp_rp"]) for r in rows])
    snr_min = st.slider("min parallax S/N (ϖ / σϖ)", 5.0, 60.0, 10.0, 1.0)
    keep = plx / err > snr_min
    d = E["cluster"].cluster_distance(plx[keep], err[keep])
    M_G = E["cluster"].absolute_magnitude(g[keep], plx[keep])
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.plot(bp_rp[keep], M_G, ".", ms=3, color="0.3")
    ax.invert_yaxis(); ax.set_xlabel("BP − RP"); ax.set_ylabel("absolute G")
    st.pyplot(fig)
    st.metric("distance / members kept", f"{d:.1f} pc  /  {keep.sum()}", help="literature 136.2 pc")


def panel_hubble(E):
    st.subheader("Hubble's law — Cosmicflows-3")
    st.caption("Change the distance range; the slope H0 (and its bootstrap error) update live.")
    arr = load_csv("05_hubble", "cosmicflows3.csv")
    dist, vel = arr[:, 0], arr[:, 1]
    dmax = st.slider("max distance (Mpc)", 50.0, 200.0, 200.0, 5.0)
    keep = dist <= dmax
    H0 = E["hubble"].fit_h0(dist[keep], vel[keep])
    med, lo, hi = E["hubble"].bootstrap_h0(dist[keep], vel[keep], n_boot=1000)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(dist[keep], vel[keep], ".", ms=4, color="0.4", alpha=0.6)
    xx = np.array([0, dist[keep].max()])
    ax.plot(xx, H0 * xx, "-", color="crimson", lw=2)
    ax.set_xlabel("distance (Mpc)"); ax.set_ylabel("velocity (km/s)")
    st.pyplot(fig)
    st.metric("H0", f"{H0:.1f} (+{hi-med:.1f}/-{med-lo:.1f}) km/s/Mpc", help="Planck 67.4, local ~73")


def panel_blackbody(E):
    st.subheader("Blackbody — the CMB temperature")
    st.caption("Drag the temperature; the Planck curve only matches FIRAS at T = 2.725 K.")
    arr = load_csv("06_blackbody", "firas_cmb.csv")
    freq, intensity, unc = arr[:, 0], arr[:, 1], arr[:, 2]
    T = st.slider("temperature (K)", 2.0, 3.5, 2.725, 0.005)
    grid = np.linspace(freq.min(), freq.max(), 300)
    model = E["blackbody"].planck_MJy(grid, T)
    chi2 = float(np.sum(((intensity - E["blackbody"].planck_MJy(freq, T)) / unc) ** 2))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(freq, intensity, yerr=unc * 400, fmt="o", color="0.2", ms=4, label="FIRAS (err ×400)")
    ax.plot(grid, model, "-", color="crimson", lw=2, label=f"Planck T={T:.3f} K")
    ax.set_xlabel("frequency (cm⁻¹)"); ax.set_ylabel("intensity (MJy/sr)"); ax.legend()
    st.pyplot(fig)
    st.metric("χ² to FIRAS", f"{chi2:,.0f}", help="minimized at the true CMB temperature")


PANELS = {
    "🪐 Transit (Kepler-8 b)": panel_transit,
    "✨ Cepheid period (V1154 Cyg)": panel_period,
    "🔭 Photometry (M67)": panel_photometry,
    "🌌 CMD (Pleiades)": panel_cmd,
    "📈 Hubble's law (H₀)": panel_hubble,
    "🌡️ Blackbody (CMB)": panel_blackbody,
}


def main():
    st.set_page_config(page_title="Astronomy demos", layout="centered")
    st.title("Astronomy demos — interactive")
    st.write("Six classic measurements, live. Every panel calls the **same tested "
             "functions** as the demos. Pick one from the sidebar and drag a slider.")
    choice = st.sidebar.radio("demo", list(PANELS))
    st.sidebar.markdown("---")
    st.sidebar.caption("Runs fully offline on bundled real data. "
                       "Code: `scripts/*.py` in each demo folder.")
    PANELS[choice](estimators())


main()
