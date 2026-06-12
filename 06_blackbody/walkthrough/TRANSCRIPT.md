# Annotated transcript — blackbody fit

A real slice of building this demo, centered on the units bug that actually happened.

- **🧑 You** · **🤖 Claude** · `> note`

---

🧑 **You:** *(step 3)* "Implement `planck_MJy` and `fit_temperature`, pass the tests."

🤖 **Claude:** Wrote the Planck law in CGS and returned it directly. Ran pytest:
```
FAILED test_recovers_injected_temperature - curve_fit: RuntimeError, T → 1.7e6
FAILED test_planck_matches_astropy        - assert 3.9e-15 == 383.5 ± 0.04
```
"The fit won't converge. Let me give it a better initial guess and bump maxfev."

> ⚠️ **The wrong turn.** A failing fit *and* a model that's ~17 orders of magnitude
> below the data is not an initial-guess problem. Look at the second test: our Planck
> value is 3.9e-15 where astropy says 383.5. That ratio is the bug.

🧑 **You:** "Don't touch maxfev. Our planck value is 3.9e-15, astropy's is 383. What
are the units of each?"

🤖 **Claude:** "Ours is CGS radiance (erg/s/cm²/Hz/sr); the data and astropy are in
MJy/sr. 1 MJy = 1e-17 erg/s/cm²/Hz, so I'm off by exactly that factor. Dividing the
CGS radiance by 1e-17..." Both tests passed; the fit returned T = 2.7250 K.

> The "non-convergence" was a symptom; the disease was units. The *absolute* astropy
> comparison diagnosed it instantly — a shape-only check would have passed and shipped a
> wrong absolute scale.

---

🧑 **You:** *(step 6)* "Look at firas_fit.png — is the fit good?"

🤖 **Claude:** "The points sit exactly on the Planck curve — and that's with the error
bars magnified ×400 to even be visible. The residuals are a few kJy/sr against a
~380,000 kJy/sr peak: under 0.01%. The CMB is a blackbody to extraordinary precision,
which is one of the strongest pieces of evidence for the hot Big Bang."

> Reading the figure as physics, not just 'the line fits.' The flatness *is* the result.

---

### Takeaways

1. A model off by many orders of magnitude is a **units bug**, not a fit-tuning problem.
   Never reach for maxfev/initial guesses to mask it.
2. Compare against the reference in *absolute* units — a shape-only check hides scale errors.
3. The famous FIRAS plot earns its fame: error bars smaller than the markers, residuals
   under 0.01%.
