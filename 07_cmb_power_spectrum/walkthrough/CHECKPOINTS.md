# Checkpoint tags — CMB map → power spectrum

> This demo was **rebuilt** from a binned-spectra version after a user correction (compute from
> the Nside-2048 maps; show the spherical-harmonic decomposition). The tags below mark the
> rebuilt, map-based pipeline. The pivot — and the intermediate problems it surfaced — is
> documented in `TRANSCRIPT.md`. (`PROMPTS.md` lays out the build as six conceptual steps; the
> reference repo groups them into the tags below.)

```bash
git checkout 07-cmb-step-1      # the spherical-harmonic pipeline + its tests
git diff   07-cmb-step-1 -- 07_cmb_power_spectrum/project/scripts/powerspectrum.py
git checkout main
```

| Tag | Captures |
|-----|----------|
| `07-cmb-step-1` | `powerspectrum.py` (the SHT pipeline) + tests: `cl_from_alm` vs healpy, recover input spectrum, NaMaster agreement |
| `07-cmb-step-2` | `make_synthetic.py`: decompose an Nside-2048 map → committed bandpowers + params.json |
| `07-cmb-step-3` | `cosmofit.py` + test: fit ΛCDM to the map-derived bandpowers, recover injected cosmology |
| `07-cmb-step-4` | `make_figures.py` + `results/` (map+spectrum, masking/NaMaster, cosmology fit) + best_fit.json |
| `07-cmb-step-5` | downgraded real Planck SMICA map + `fetch_real_map.py`; real-data peak |
| `07-cmb-step-6` | `notebook.ipynb`, PLAN/README/notes/walkthrough (incl. the intermediate-problems catalog) |

> The pixel-window bias (a real 2% error) and the binning artifact (a *fake* 5% bias) were both
> fixed while building `powerspectrum.py` / `make_synthetic.py` — see `TRANSCRIPT.md` for why
> they needed opposite responses.
