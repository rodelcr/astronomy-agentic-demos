# Annotated transcript — period of a Cepheid

A real slice of building this demo, centered on the bug that actually happened.

- **🧑 You** · **🤖 Claude** · `> note`

---

🧑 **You:** *(step 3)* "Implement `string_length_period` and make the tests pass."

🤖 **Claude:** Wrote a first version summing `np.hypot(dphase, dmag)` over phase-sorted
points. Ran pytest:
```
FAILED test_recovers_injected_period - assert 5.41 == 3.7 ± 0.037
```
"The recovered period is wrong. Let me try a finer period grid."

> ⚠️ **The wrong turn.** A finer grid won't help if the *metric* is broken. Before
> changing resolution, look at the metric itself:

🧑 **You:** "Plot string length vs trial period. Is there even a clear minimum at 3.7?"

🤖 **Claude:** *(plots)* "The curve is almost flat — there's no real minimum. The
problem is scale: phase spans 0–1 but magnitude spans only ~0.3, yet I'm adding them
with equal weight, so the Δmag term barely moves and the metric is dominated by the
Δphase term, which is similar for every period. I should normalize the magnitude axis
by its range." Changed to `np.hypot(dphase, dmag / span)`.
```
2 passed
```

> The fix wasn't more compute — it was realizing the two axes had incomparable units.
> The diagnostic plot (a flat periodogram) made that obvious in one look.

---

🧑 **You:** *(step 6)* "Our string-length period is 4.9252 d but Lomb-Scargle gives
4.9124 d. Which is right?"

🤖 **Claude:** "They agree to 0.26%, and the literature is 4.9254 d — so string-length
is spot on here. The small Lomb-Scargle offset comes from residual instrumental
trends in the SAP flux over the quarter, which tilt the Fourier periodogram slightly.
Both are 'right' to within the systematics; the agreement is what matters."

> The honest answer: two methods agreeing to a fraction of a percent *is* the result.
> Don't over-claim a 4th decimal place the data can't support.

---

### Takeaways

1. When a fit is wrong, suspect the **metric** before the **resolution**.
2. A flat periodogram is a diagnostic, not a failure — it told us the units were off.
3. Independent methods agreeing (string-length vs Lomb-Scargle) is far stronger than
   one method quoted to many decimals.
