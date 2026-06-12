# Interactive dashboard

A Streamlit app that turns the six demos into live, slider-driven visualizations. Every
panel calls the **same tested functions** as the demos (`scripts/*.py` in each demo
folder), so the picture on screen is the code `pytest` verifies — not separate,
untrusted visualization math.

## Run it

```bash
conda activate demos
streamlit run gui/app.py
```

A browser tab opens at `http://localhost:8501`. Pick a demo from the sidebar and drag a
slider. Everything runs **offline** on the bundled real data — no network, no API, no
live model.

## The panels

| Panel | Drag this | Watch |
|-------|-----------|-------|
| 🪐 Transit (Kepler-8 b) | period, t0 | the folded transit smear when the period is wrong; Rp/R* |
| ✨ Cepheid (V1154 Cyg) | trial period | the light curve collapse into one clean cycle; string-length minimum |
| 🔭 Photometry (M67) | aperture & annulus radii | the measured flux change as the aperture grows |
| 🌌 CMD (Pleiades) | parallax S/N cut | the main sequence tighten as field stars drop out; distance |
| 📈 Hubble (H₀) | max distance | the slope H₀ and its bootstrap error update live |
| 🌡️ Blackbody (CMB) | temperature | the Planck curve fit FIRAS only at 2.725 K; χ² minimized |

## If something goes wrong on stage

- **"streamlit: command not found"** → you're not in the env. `conda activate demos`.
- **Port busy** → `streamlit run gui/app.py --server.port 8600`.
- **Blank/odd page** → hard-refresh the browser, or restart with `Ctrl-C` then re-run.
- **No GUI at all** → every panel's computation also lives in the demo notebooks and
  `scripts/*.py`; fall back to those.

## Rebuilding / extending it

See `gui/PROMPT.md` for a ready-to-paste prompt that builds this app from scratch with
an agent, plus follow-up prompts to extend it live.
