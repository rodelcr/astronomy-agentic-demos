# Annotated transcript — <demo title>

One real, lightly-edited session building this demo with Claude Code. It includes
a **wrong turn** and how it got caught — because that's what real sessions look
like. Margin notes in `> blockquotes` explain what's happening.

Format:
- **🧑 You** — what you typed
- **🤖 Claude** — a condensed version of what it did
- `> note` — the teaching point

---

🧑 **You:** *(Step 1 prompt — repo + failing test)*

🤖 **Claude:** Initialized git, wrote the stub and the test, ran pytest:
```
FAILED tests/test_<name>.py::test_recovers_injected - assert None == <value>
```

> The test fails because the stub returns `None`. Good — that's the *right* kind
> of failure. If it had failed with `ImportError` you'd fix plumbing, not physics.

---

🧑 **You:** *(Step 4 — inspect the figure)* "Look at results/fit.png — is this good?"

🤖 **Claude:** "The fit looks reasonable, the model passes through the points."

> ⚠️ **The wrong turn.** Claude declared victory from a thumbnail. Don't accept
> "looks reasonable." Push on the residuals:

🧑 **You:** "Plot the residuals (data − model) underneath, on their own axis. Don't
tell me it's good until I can see no structure in them."

🤖 **Claude:** *(re-plots)* "You're right — the residuals show a clear <trend>.
That points to <cause>. Let me fix <thing> and re-fit."

> This is the entire lesson of habit #3. The agent will happily rationalize a bad
> fit. Your job is to demand the diagnostic plot that would expose it.

---

🧑 **You:** *(Step 7 — external validation)*

🤖 **Claude:** Added a test comparing our result to `<library>`; they agree to
`<tolerance>`. "Our value is X, <library> gives Y."

> Now there are two independent checks: synthetic ground truth *and* a trusted
> library. Either alone can mislead; together they're convincing.

---

### What to take away

1. "Looks good" is not a result. A residual plot is.
2. The agent is a fast, tireless pair-programmer — and an uncritical one. The
   skepticism has to come from you.
3. Every claim ended up backed by a test you can re-run. That's the difference
   between a demo and a result.
