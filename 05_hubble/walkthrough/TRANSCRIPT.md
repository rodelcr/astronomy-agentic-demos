# Annotated transcript — Hubble's law

A real slice of building this demo, centered on the mistake that actually happened.

- **🧑 You** · **🤖 Claude** · `> note`

---

🧑 **You:** *(step 3)* "Implement `fit_h0` and pass the tests."

🤖 **Claude:** "I'll use `scipy.stats.linregress` — it's the standard linear fit."
Wrote it, returning `.slope`. Ran pytest:
```
FAILED test_recovers_injected_H0 - assert 68.7 == 70.0 ± 3.5   (passed, barely)
                                 - intercept = 412 km/s (nonzero!)
```
"It passes the slope check. Good enough."

> ⚠️ **The wrong turn.** `linregress` fits a *free intercept* — and it came out at 412
> km/s, which is unphysical (a galaxy at zero distance isn't receding at 412 km/s). The
> nonzero intercept tilts the slope. "Barely passes" with a physically wrong intercept
> is a red flag, not a green light.

🧑 **You:** "Our model is v = H₀ d, through the origin. linregress is fitting an
intercept we know is zero. Use a through-origin least squares instead and check the
slope changes."

🤖 **Claude:** "Right. Forcing through the origin, H₀ = Σ(d·v)/Σ(d²) — closed form, no
intercept. The slope moves to 74.8 and now matches scipy's `curve_fit(v=H*d)` exactly."

> Encoding the physics (intercept ≡ 0) wasn't a detail — it changed H₀ by several
> km/s/Mpc. The scipy cross-check, with the *right* model, is what confirmed it.

---

🧑 **You:** *(step 6)* "Our error bar is ±0.8. So we've measured H₀ to 1%?"

🤖 **Claude:** "Statistically, yes — the bootstrap says the *slope* is pinned to ±0.8
under resampling. But that's not the real uncertainty on H₀: it ignores systematic
errors in the distance scale, which are the whole story behind the Hubble tension
(local ~73 vs Planck 67.4). I shouldn't claim a 1% measurement of H₀."

> The crucial honesty: a tight statistical error bar is not a small *total* error.
> Distinguish what your method constrains from what it doesn't.

---

### Takeaways

1. Encode the physics you know (the line goes through the origin) — it's not pedantry,
   it moved H₀ by several units.
2. "Barely passes" + an unphysical nuisance parameter = a bug, not a pass.
3. A bootstrap measures *statistical* scatter, not *systematic* error. Don't sell a
   small error bar as a small uncertainty.
