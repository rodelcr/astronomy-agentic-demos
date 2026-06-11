"""<name>.py — <one-line description of the estimator>.

Designed to be BOTH importable and runnable as a CLI:

    from scripts.<name> import measure          # in a notebook or test
    python scripts/<name>.py --data data/real/...   # from the shell

Replace this template when you copy it into a real demo.
"""
from __future__ import annotations

import argparse


def measure(...):
    """Core measurement. Pure function: data in, number(s) out.

    Keep this free of plotting and file I/O so it's trivial to test.
    """
    raise NotImplementedError


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", required=True, help="path to the input data file")
    # ... demo-specific flags ...
    args = p.parse_args()
    result = measure(...)
    print(result)


if __name__ == "__main__":
    _main()
