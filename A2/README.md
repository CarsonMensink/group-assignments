# CMP_SC 4050 — Group Algorithm Engineering Assignment 2

**From Brute Force to Better Algorithms: Divide and Conquer + Dynamic Programming**

The engineering report is [`Report.pdf`](Report.pdf). This folder holds all
source code, experiment scripts, and the machine-readable results behind the
report's tables and figures.

## Requirements

- **Language:** Python **3.10 or newer**. **No third-party packages:** everything
  uses the standard library, including the SVG plots.
- **Version used for the submitted results:** Python 3.14.3 on an Apple M3
  (macOS, arm64), for both the Part I and Part 2C timings. All scripts were
  rerun from a clean copy of this folder with that version.
- Run with normal `python3`. `python3 -O` strips the `assert` statements that the
  validation suites rely on.

## Reproducing the Experiments

Run these from this `A2` folder. Every script finds its own files and imports,
so they also work from any other working directory.

```sh
python3 part-1/main.py                  # Part 1B: validation + benchmark (~1 min) + plots
python3 part-2/2b/main.py               # Part 2B: exact-solver validation + greedy counterexample search
python3 part-2/2c/part2c_experiments.py # Part 2C: memoization + pseudo-polynomial experiments
```

`python3 part-1/main.py --validate` runs only the Part 1 validation, which takes a
few seconds. Part 2A has no runner of its own: its solvers are exercised by 2B and
2C.

| Part | Script | Random seed(s) | Output files (overwritten on rerun) |
| --- | --- | --- | --- |
| 1A | `part-1/1a/inversions.py` | — | (library; `python3 part-1/1a/inversions.py` runs a demo) |
| 1B | `part-1/main.py` | validation `4050`, benchmark `2026` | `part-1/1b/validation_results.csv`, `benchmark_results.csv`, `benchmark_raw.csv`, `runtime_loglog.svg`, `speedup.svg`, `normalized.svg` |
| 2A | `part-2/2a/algorithms.py` | — | (library) |
| 2B | `part-2/2b/main.py` | `4050` | `part-2/2b/greedy_counterexamples.csv` |
| 2C | `part-2/2c/part2c_experiments.py` | `42` | `part-2/2c/part2c_experiment1.csv`, `part2c_experiment2.csv` |

Counts, validation results, and counterexamples are deterministic and reproduce
exactly. Runtimes depend on the hardware, the Python version, and system load, so
rerunning the timing experiments changes the timing columns but not the trends.

## Contents

| Path | What it is |
| --- | --- |
| [`part-1/`](part-1/README.md) | **Part I: inversion counting.** Brute-force and divide-and-conquer counters (1A), validation, benchmark, and graphs (1B) |
| [`part-2/2a/`](part-2/2a/README.md) | **Part 2A: four coin-change solvers** (greedy, naive recursion, top-down memo, bottom-up DP) with complexity analysis |
| [`part-2/2b/`](part-2/2b/README.md) | **Part 2B: exact-solver cross-validation** and automated greedy counterexample search |
| [`part-2/2c/`](part-2/2c/README.md) | **Part 2C: memoization instrumentation** and pseudo-polynomial scaling experiments |
| [`part-3/`](part-3/Cross-Paradigm-Engineering-Reflection.md) | **Part III: cross-paradigm reflection** |
| `Report.pdf` | Engineering report, including the contribution and AI use statements |
