# Prompt walkthrough — CMB map → power spectrum (capstone)

The agentic-coding side. Paste each step into Claude Code in your own empty folder, one at a
time; read the diff and look at the output before continuing. This is the most ambitious demo:
you compute a power spectrum from a sky **map** by spherical-harmonic decomposition, validate
against `healpy` and **NaMaster**, then fit a cosmology. Expect intermediate problems — that's
the point; see `TRANSCRIPT.md`.

> Arc: **the SHT estimator → make a sky → decompose it → masking/NaMaster → fit cosmology → real sky.**

### Step 0 — Orient
```
Read 07_cmb_power_spectrum/PLAN.md and project/README.md. What are we computing, by what
transform, and what two libraries validate it? Why do we NOT use Planck's pre-binned spectra? No code.
```
**Look for:** "spectrum from a map via spherical-harmonic decomposition; validated by
healpy.alm2cl and NaMaster; binned spectra hide the computation."

### Step 1 — The estimator first (and validate it)
```
Write scripts/powerspectrum.py with cl_from_alm(alm): compute Ĉ_ℓ = 1/(2ℓ+1) Σ_m |a_ℓm|² BY HAND
(HEALPix stores only m≥0, so it's |a_{ℓ0}|² + 2 Σ_{m≥1} |a_ℓm|²). Write a test asserting it
matches healpy.alm2cl on a small map. Run pytest. Commit "step 1: cl_from_alm + healpy check".
```
**Look for:** machine-precision agreement. The decomposition must be real, inspectable code.

### Step 2 — Make a sky and decompose it
```
Add generate_cmb_map (synfast from a CAMB C_ℓ — APPLY the pixel window so it behaves like a real
map), map_to_alm, pixel_window, bin_spectrum. Write a test: synthesize a map from a known C_ℓ,
decompose it back, and recover the input (bin the input the SAME way to compare!). Commit "step 2".
```
**Look for:** the two traps in TRANSCRIPT — apply pixwin at generation (or the spectrum tilts
high), and compare binned-to-binned (or a steep spectrum fakes a 5% bias).

### Step 3 — Masking and NaMaster
```
Add pseudo_cl (Ĉ_ℓ of map·mask, divided by f_sky) and namaster_bandpowers (NaMaster MASTER
deconvolution). Write a test: on a Galactic-cut apodized mask, our fsky estimator agrees with
NaMaster to ~10%. Commit "step 3: masking + NaMaster".
```
**Look for:** NaMaster is the rigorous answer; the residual fsky-vs-MASTER difference is the
mode-coupling. (API note: `NmtBin.from_nside_linear(nside, nlb)` — no `lmax` kwarg.)

### Step 4 — The data product: decompose an Nside-2048 map
```
Write data/synthetic/make_synthetic.py: synthesize a polarized Nside-2048 map from a chosen
cosmology, run the pipeline to get TT (hand-rolled) and TE (healpy spin-2) bandpowers, save them
+ params.json. The map is 400 MB — DON'T commit it; commit the bandpowers. Commit "step 4".
```
**Look for:** the committed data is the small spectrum measured off the map, not the map.

### Step 5 — Fit a cosmology to the map-derived spectrum
```
Write scripts/cosmofit.py: CAMB theory + fit_cosmology over {H0, ωc, As} with cosmic-variance
errors. Write a test: fit the bandpowers from step 4 and recover the injected cosmology. Commit
"step 5: cosmology fit".
```
**Look for:** recovers the injected H₀ (~69). If it lands several km/s/Mpc off, suspect a
pipeline bias (step 2's pixel window) — not the fit.

### Step 6 — Figures, the real sky, and notes
```
Write scripts/make_figures.py (map+spectrum, masking/NaMaster, cosmology fit, real SMICA) and
scripts/fetch_real_map.py (download SMICA, downgrade to Nside 256). Run the real map through the
pipeline. Then write notes/ — including a catalog of the intermediate problems you hit and how
you solved them. Commit "step 6: figures + real map + notes".
```
**Look for:** the first acoustic peak from real Planck data, and an honest write-up of the messy
steps (that catalog is the agentic-coding lesson).

---
`git tag` lists `07-cmb-step-1 … -step-6`. Diff vs the reference:
```
git diff 07-cmb-step-1 -- 07_cmb_power_spectrum/project/scripts/powerspectrum.py
```
