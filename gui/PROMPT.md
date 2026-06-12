# Ready-to-go prompt — build the visualization GUI with an agent

Two ways to use this file:

1. **You have a model (Claude Code) live.** Paste the **Master prompt** below and let
   the agent build `gui/app.py`. Use the follow-ups to extend it on stage.
2. **No model / no network.** The GUI is already built and committed at `gui/app.py` —
   just run it (see `gui/README.md`). This file then doubles as documentation of intent.

---

## Master prompt (copy-paste)

```
Build a Streamlit dashboard at gui/app.py that turns the six astronomy demos in this
repo into live, slider-driven visualizations. Hard requirements:

- REUSE the demos' own tested functions — import each estimator from
  <demo>/project/scripts/*.py (transit.py, variable.py, photometry.py, cluster.py,
  hubble.py, blackbody.py). Do NOT reimplement the science in the GUI; the whole point
  is that what's on screen is the code the tests verify. Load each module by file path
  (importlib) so the per-demo `scripts/` packages don't collide.
- Run fully OFFLINE on the bundled real data in each demo's data/real/. No network, no
  API calls, no live model.
- One panel per demo, chosen from a sidebar radio. Each panel: a short caption, an
  interactive control, a matplotlib figure (st.pyplot), and an st.metric showing the
  headline number with the literature value in its help text.

Panels and their key interaction:
  1. Transit (Kepler-8 b): sliders for period and t0 → live phase fold + trapezoid fit;
     metric = recovered Rp/R* (lit 0.0944). Dragging period off 3.52254 d smears the fold.
  2. Cepheid (V1154 Cyg): slider for trial period → folded light curve; optional
     checkbox to show the string-length periodogram with the minimum marked (lit 4.9254 d).
  3. Photometry (M67): sliders for aperture radius and sky annulus → aperture overlay on
     a zoomed star + measured flux/instrumental mag.
  4. CMD (Pleiades): slider for a minimum parallax S/N cut → CMD that tightens as field
     stars are removed; metric = distance (lit 136.2 pc) and members kept.
  5. Hubble (Cosmicflows-3): slider for max distance → Hubble diagram + fit line;
     metric = H0 with bootstrap error (Planck 67.4, local ~73).
  6. Blackbody (CMB/FIRAS): slider for temperature → Planck curve over the FIRAS points
     (error bars ×400) + a live χ² metric, minimized at T = 2.725 K.
  7. CMB spectrum (Planck, capstone): slider for H0 → CAMB ΛCDM theory over the Planck TT
     acoustic peaks + a live χ² metric, minimized near H0 = 67 (cache the CAMB call by
     parameters with st.cache_data so the slider stays responsive). Ties to panel 5: this
     is the early-Universe H0 vs the local one — the Hubble tension.

Then verify it WITHOUT a browser using streamlit.testing.v1.AppTest: load the app, select
each sidebar option, and assert `at.exception is None` for every panel. Finally boot it
headless (streamlit run ... --server.headless true) and confirm it serves HTTP 200.
Commit as "add interactive Streamlit dashboard".
```

## Follow-up prompts (extend it live)

```
Add a "smear meter" to the transit and Cepheid panels: a number that quantifies how
well the current period folds the data (e.g. the binned scatter), so students can hunt
for the minimum by feel.
```
```
Add an "isochrone" overlay slider to the CMD panel: draw a simple theoretical main
sequence and let the user slide the cluster age; note this needs an isochrone table, so
bundle a small one and cite it.
```
```
Add a download button under each figure that saves the current view to results/ so a
student can capture the exact parameters they explored.
```

## Why these choices (say this to the room)

- **The GUI imports the tested code.** No "demo-only" math that could quietly disagree
  with the real pipeline — the slider drives the exact function `pytest` checks.
- **Offline by design.** A live demo that depends on a network or an API will fail at
  the worst moment; everything here runs from committed data.
- **Sliders teach the failure mode.** Watching the transit fold *smear* when the period
  is wrong, or χ² *climb* when the CMB temperature is off, builds the intuition the
  static figures can't.
