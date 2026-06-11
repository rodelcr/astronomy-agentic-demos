# Checkpoint tags — <demo title>

The reference `project/` was built one commit per prompt step, each marked with a
git tag. Rewind to any of them to see the project at that stage, or diff your own
work against them.

```bash
git checkout <NN>-<name>-step-5      # look at the project after step 5
git diff   <NN>-<name>-step-5 -- .   # what changed since then
git checkout main                    # back to the finished version
```

| Tag | Captures (after this step the project has…) |
|-----|---------------------------------------------|
| `<NN>-<name>-step-1` | repo + a failing synthetic-recovery test |
| `<NN>-<name>-step-2` | synthetic data generator + `params.json` ground truth |
| `<NN>-<name>-step-3` | notebook exploration + first figure |
| `<NN>-<name>-step-4` | residual-diagnosed, corrected fit |
| `<NN>-<name>-step-5` | logic refactored into `scripts/<name>.py` with a CLI |
| `<NN>-<name>-step-6` | synthetic-recovery test passing (green) |
| `<NN>-<name>-step-7` | external-library agreement test passing |
| `<NN>-<name>-step-8` | run on real data + final figure |
| `<NN>-<name>-step-9` | notes + handoff written |

> Note: the reference repo's *whole history* is the construction story. Try
> `git log --oneline --decorate` to read it like a lab notebook.
