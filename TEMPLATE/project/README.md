# <Demo title> — <one-line problem statement>

## The problem

<2–4 sentences: what astronomical quantity are we measuring, from what data?>

## Physics scaffold

<A short, honest scaffold for an undergrad. The one or two equations that matter,
with every symbol defined. Keep it to what's needed to understand the code.>

> Headline result: **<quantity> = <value> ± <error> (<unit>)**

## What's in here

```
project/
  notebook.ipynb        exploratory narrative — read this first to see the thinking
  scripts/<name>.py     the trusted implementation: importable function + CLI
  tests/test_<name>.py  synthetic-recovery test + external-library agreement test
  data/
    real/               bundled real data (runs offline)
    synthetic/          seeded generator + params.json ground truth
  results/              committed figures — inspect these
  notes/                NOTES (what was tried) + HANDOFF (the result)
  requirements.txt      pinned deps (superset is the repo-root environment.yml)
```

## Run it

```bash
conda activate demos
pytest
python scripts/<name>.py --help
```

## External answer key

This demo validates its result against **<library>** — see
`tests/test_<name>.py`.
