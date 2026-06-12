# Annotated transcript — CMB power spectrum

A real slice of building the capstone, centered on the units bug and the honesty call.

- **🧑 You** · **🤖 Claude** · `> note`

---

🧑 **You:** *(step 4)* "Overlay the CAMB theory on the Planck TT data."

🤖 **Claude:** Pulled CAMB's `get_cmb_power_spectra(..., raw_cl=True)` and plotted it. "The
theory is essentially flat near zero compared to the data peaks at ~5000. Let me multiply by
a constant to bring it up to the data."

> ⚠️ **The wrong turn.** Rescaling by a fudge constant would *hide* the real issue and make
> the fit meaningless. The data are **D_ℓ = ℓ(ℓ+1)C_ℓ/2π in μK²**; CAMB's `raw_cl` output is
> the dimensionless **C_ℓ**. The mismatch isn't amplitude — it's the wrong quantity *and* the
> wrong units.

🧑 **You:** "Don't rescale. What are the units and the ℓ-weighting of each curve? The data
column is D_ℓ in μK²."

🤖 **Claude:** "Right — I need D_ℓ = ℓ(ℓ+1)C_ℓ/(2π), and to convert dimensionless C_ℓ to μK²
with the (2.7255×10⁶)² factor (or just ask CAMB for `CMB_unit='muK'`, which returns D_ℓ
directly). With that, the theory lands right on the peaks." `test_normalization_matches_camb`
now guards it.

> The ℓ(ℓ+1)/2π weighting and the μK² scale are *the* first CMB gotcha. A constant rescale
> would have "worked" visually and poisoned every parameter downstream.

---

🧑 **You:** *(step 6)* "We got H₀ = 67.0 ± … with χ²/dof = 1.09. So we've reproduced Planck?"

🤖 **Claude:** "We've reproduced Planck's *central values* with a simplified fit — but I
shouldn't call this 'reproducing Planck.' We used a Gaussian likelihood on the binned public
spectra with diagonal errors, no bandpower windows, and fixed ωb, nₛ, τ. The real Planck
likelihood has a full covariance and ~20 nuisance parameters and is sampled by MCMC. Our
central values agree; our error bars are illustrative. I'll state that in the README and notes."

> The honesty *is* the deliverable here. A fit that lands on the right number with unstated
> assumptions is a worse scientific artifact than a wider fit with its caveats written down.

---

### Takeaways

1. When theory and data are orders of magnitude apart, check the **quantity and units**
   (C_ℓ vs D_ℓ, K vs μK) before rescaling. Never fudge a constant to match.
2. The external code (CAMB) is the *model* here — so the testable, student-owned piece is the
   normalization, and that's exactly what we validate.
3. Reproducing a *number* is not reproducing an *analysis*. Name every simplification; the
   honesty is graded higher than the digits.
