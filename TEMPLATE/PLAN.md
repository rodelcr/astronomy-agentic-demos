# Plan — <demo title>

> This is the **design doc** for the demo: what we're building and why, written
> *before* any code. In Claude Code this is what you produce in **plan mode**
> (and approve with ExitPlanMode) before the agent touches a file. The
> `walkthrough/PROMPTS.md` steps are this plan, executed. Read this first.

## Context

<Why this problem? What does the student learn? What's the headline quantity and
the one external library we validate against? 3–6 sentences.>

## The science (what we're measuring)

- **Input data:** <real dataset + the synthetic stand-in with known answer>
- **Method:** <the estimator/fit, in one or two lines>
- **Headline output:** <quantity> = <value> ± <error> (<unit>)
- **External answer key:** <library> — why it's trustworthy

## Approach (and the alternative we rejected)

- **Chosen:** <the approach we take and why it fits an undergrad demo>
- **Rejected:** <a plausible alternative + one-line reason it's worse here>

## Components

| File | Responsibility |
|------|----------------|
| `data/synthetic/make_synthetic.py` | seeded generator + `params.json` ground truth |
| `scripts/<name>.py` | the estimator: importable function + argparse CLI |
| `tests/test_<name>.py` | (a) recover injected truth; (b) agree with `<library>` |
| `notebook.ipynb` | exploratory narrative; imports the script function |
| `results/` | committed figures (fit + residuals) |
| `notes/` | NOTES + HANDOFF |

## Build steps

Mirror `walkthrough/PROMPTS.md` (steps 1–9), each a commit + checkpoint tag:
failing test → synthetic data → notebook explore → inspect/iterate figure →
refactor to script+CLI → synthetic test green → external-library test →
real data run → notes.

## Verification

- `pytest` passes: synthetic-recovery **and** external-library-agreement tests.
- `python scripts/<name>.py --help` runs; notebook executes headless
  (`jupyter nbconvert --execute`).
- `results/` figures show the fit and flat residuals.
- Runs offline (bundled data only).

## Risks / notes

<Anything fiddly: data trimming size, numerical tolerances, units/frames.>
