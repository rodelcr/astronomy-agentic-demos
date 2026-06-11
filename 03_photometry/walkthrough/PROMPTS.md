# Prompt walkthrough — aperture photometry

The agentic-coding side. Paste each step into Claude Code in your own empty folder,
one at a time; read the diff and look at the output before continuing. Compare against
`../project/` and `CHECKPOINTS.md`.

> Arc: **tests first → data → implement → explore → inspect → real data → notes.**

### Step 0 — Orient
```
Read 03_photometry/PLAN.md and project/README.md. What are we measuring, how, and what
library do we validate against? No code yet.
```
**Look for:** "aperture sum minus sky annulus, validated against photutils."

### Step 1 — Tests first (red)
```
Write tests/test_photometry.py with two tests + a stub scripts/photometry.py so they
import and fail:
  1. test_recovers_relative_photometry — measure synthetic stars of known flux, assert
     recovered magnitude DIFFERENCES match the truth (aperture loss cancels).
  2. test_agrees_with_photutils — assert our raw aperture sum matches photutils
     CircularAperture (method='center') exactly.
Run pytest, show me red. Commit "step 1: failing tests".
```
**Look for:** why *differences*, not absolute flux? Make sure the agent can explain it.

### Step 2 — Synthetic star field with known fluxes
```
Write data/synthetic/make_synthetic.py: place a few 2-D Gaussian stars of KNOWN total
flux on a flat sky + noise, seeded. Save starfield.npy and params.json (positions +
fluxes). Run it. Commit "step 2: synthetic field + ground truth".
```
**Look for:** the PSF is normalized so each star's pixels sum to its stated flux.

### Step 3 — Implement photometry (green)
```
Implement scripts/photometry.py: aperture_flux(image,x,y,r,r_in,r_out) summing pixels
in a circle minus the median sky annulus; aperture_flux_raw (no sky); instrumental_mag;
measure(...) over a list of positions. Make both tests pass; add a CLI that detects
stars with DAOStarFinder and prints magnitudes. Commit "step 3: photometry passes".
```
**Look for:** the pixel-edge convention (see TRANSCRIPT). Use strict `<` so the
aperture matches photutils' `method='center'` exactly. `--help` works.

### Step 4 — Explore + weave in the notebook
```
Create notebook.ipynb: load data/real/m67_cutout.fits, display it with a sqrt stretch,
detect stars, measure one by hand IMPORTING from scripts/photometry.py, then cross-check
all of them against photutils. Commit "step 4: notebook".
```
**Look for:** notebook imports the script's functions; the cross-check prints a
near-zero max difference.

### Step 5 — Inspect the apertures
```
Write scripts/make_figures.py: results/apertures.png (image with apertures + sky annuli
overlaid on the brightest stars) and results/compare.png (our sums vs photutils, 1:1).
Look at apertures.png: are the circles ON the stars and the annuli free of neighbors?
Commit "step 5: figures".
```
**Look for:** misplaced circles or annuli sitting on a neighbor = a real problem. The
overlay is the inspection.

### Step 6 — Real cluster
```
Run on data/real/m67_cutout.fits, list the brightest stars' instrumental magnitudes,
and confirm our sums match photutils exactly on the real image. Commit "step 6: real M67".
```
**Look for:** max fractional difference 0. If it's ~1%, you have the `<=`/`<` bug.

### Step 7 — Notes
```
Write notes/NOTES_photometry.md (decisions + the pixel-edge gotcha) and
notes/HANDOFF_photometry.md (headline, files, reproduce, extensions).
Commit "step 7: notes".
```

---
`git tag` lists `03-photometry-step-1 … -step-7`. Diff vs reference:
```
git diff 03-photometry-step-3 -- 03_photometry/project/scripts/photometry.py
```
