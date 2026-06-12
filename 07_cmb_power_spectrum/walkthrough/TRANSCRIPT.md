# Annotated transcript — CMB map → power spectrum

This is the demo's most important document. Building the map-based pipeline meant solving a
string of **intermediate problems** — a data shortcut the user rejected, a flaky 2 GB
download, a library API quirk, and two subtle numerical biases. None of them were the
"headline" task; all of them would have silently wrecked the result. This is exactly where
an agentic coding tool earns its keep: it produces **ready-made solutions to the messy steps
between you and the answer**, and you keep it honest.

Read this top to bottom — it's the real back-and-forth, lightly edited.

- **🧑 You** · **🤖 Claude** · `> note`

---

## Problem 0 — the shortcut the user caught (the meta-lesson)

The first version of this demo fit Planck's **pre-binned** TT/TE spectra (CSV files from the
archive). It passed its tests and reproduced Planck's parameters. Then:

🧑 **You:** *"I didn't want you to use the binned spectra. I want you to compute them from the
Nside 2048 maps from Planck — actually show how you do the spherical harmonic decomposition."*

> ⚠️ The agent had optimized for "get the number" and skipped the **actual computation** —
> going from a sky map to a spectrum. The lesson for students: an agent will happily take the
> shortest path to a plausible answer. *You* decide what the lesson is. The fix was a full
> rebuild around `map → aₗₘ → Cₗ`, with the binned spectra deleted from the pipeline.

---

## Problem 1 — the spherical harmonic estimator: trust, then verify

🤖 **Claude:** Implemented `cl_from_alm` summing over m by hand,
`Ĉ_ℓ = (|a_{ℓ0}|² + 2Σ_{m≥1}|a_{ℓm}|²)/(2ℓ+1)`, because HEALPix stores only m ≥ 0.

> Rather than trust the hand-rolled m-sum, the agent validated it against `healpy.alm2cl`:
> **max abs difference 7×10⁻¹⁵** — machine precision. That's the pattern from every other demo:
> the decomposition is real, inspectable code, checked against the canonical library.

---

## Problem 2 — a 2 GB download that kept dying

To add a real-data check we needed the Planck SMICA map — a single ~2 GB HEALPix FITS file.

🤖 **Claude:** First download returned 598 MB of 2 GB; the connection had dropped. A naive read
failed: `cannot reshape array of size 31298958 into shape (50331648,)` — Planck FITS interleaves
all columns per row, so a truncated file can't yield even the temperature column.

> The ready-made solution wasn't heroics — it was a **resume-with-retries loop**
> (`curl -C - --max-time 120` in a `for` loop), run in the background while the offline core got
> built. It crept up ~15 MB per attempt (the archive throttles) and completed after ~40 tries.
> Meanwhile no time was wasted: the synthetic pipeline — the actual lesson — was finished in
> parallel. Knowing what to background and what to block on is a real skill the agent applied.

---

## Problem 3 — the NaMaster API didn't match memory

🤖 **Claude:** `nmt.NmtBin.from_nside_linear(nside, nlb, lmax=...)` →
`TypeError: unexpected keyword argument 'lmax'`.

> A one-line fix (drop the `lmax` kwarg) — but the point is the agent **read the actual error and
> adapted to the installed version (pymaster 2.7)** instead of insisting on a remembered signature.
> Libraries drift; the traceback is ground truth.

---

## Problem 4 — a "5% bias" that wasn't (binning vs. the truth)

🤖 **Claude:** The first recovery test failed: decomposed spectrum ran 5% high vs the input
theory. The instinct is "the pipeline is biased."

🧑 *(the agent pushed on itself):*

🤖 **Claude:** "Wait — I'm comparing the **bin-averaged** measurement to the theory value **at the
bin centre**. For a steeply falling spectrum the bin average is higher than the centre value
(Jensen's inequality). That's a *comparison* artifact, not a pipeline bias." Fix: bin the input
theory the **same way** before comparing. Test went green and meaningful.

> A worse engineer (or a rushed agent) would have just loosened the tolerance to 7% and shipped.
> The ready-made solution was the *right* comparison, which also taught the real lesson about
> binning.

---

## Problem 5 — a real 2% bias (the pixel window)

After fixing the comparison, a genuine **+2.2%** bias remained, and the per-band scatter (1.6%)
was ~2× the cosmic-variance error it should have had — the cosmology fit then chased it to
**H₀ = 65.4** instead of the injected 69.

🤖 **Claude:** Diagnosed it: the synthetic map was made *without* the HEALPix pixel window, but the
analysis divided by `pixwin²` anyway — over-correcting at high ℓ (where `pixwin < 1`), tilting the
spectrum up. The fix is physically correct: **make the map carry the pixel window** (apply it to
the aₗₘ before pixelizing, like a real observation), so dividing it out is exact, not a fudge.

🤖 **Claude:** After the fix: bias 2.2% → 0.5%, and the fit recovered **H₀ = 69.19** (injected 69.0),
ωc and Aₛ on the nose.

> Two biases, two completely different fixes — one a comparison artifact to *not* "fix" in the
> code, one a real physics error to fix at map generation. Telling them apart required a
> **diagnostic** (ratio of map-derived to input, mean *and* scatter vs the predicted error), not a
> tolerance knob. That diagnostic is the ready-made tool the agent reached for.

---

## What students should take from this

1. The headline ("fit the CMB") was maybe 20% of the work. The other 80% was **intermediate
   steps**: data wrangling, API drift, two numerical subtleties. An agent is fastest exactly here
   — it writes the resume loop, reads the traceback, builds the diagnostic — *if you make it
   verify instead of declare victory.*
2. Distinguish a **comparison artifact** (don't change the code) from a **real bias** (fix the
   physics). The way you tell is a diagnostic plot/number, never a tolerance.
3. The user is the source of the *goal*. The agent took a shortcut (binned spectra); the correction
   redefined the task. Keep your hand on the wheel.
