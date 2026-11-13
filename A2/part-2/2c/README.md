# Part 2C: Memoization and Pseudo-Polynomial Behavior

## How to Run

Use Python 3.10 or newer. No third-party packages are required. The script
imports the group's Part 2A solvers from `../2a/algorithms.py`, so it works from
any working directory:

```sh
python3 A2/part-2/2c/part2c_experiments.py    # from the repository root
python3 part2c_experiments.py                 # from this folder
```

Run with normal Python; `python3 -O` disables the validation assertions. The
whole script takes a few seconds.

## What It Does

1. **Validation:** 239 small cross-checks of the three exact solvers (naive,
   memoized, bottom-up). There are 39 fixed cases (targets 0–12 with
   `{1,3,4}`, `{1,4,6}`, `{4,6}`) and 200 random cases with seed `42`. All three
   must return identical results, and each bottom-up coin list is checked for
   count, sum, and allowed coins.
2. **Experiment 1 (repeated subproblems):** `COINS = [1,3,4]`, targets
   5, 10, 15, … until naive recursion hits the documented safety cutoff of
   **250,000 calls**. Instrumented copies of the naive and memoized recurrences
   count recursive calls, distinct amounts reached, and cache hits. Completed
   answers are asserted equal to the real Part 2A solvers. The memo starts with
   `{0: 0}`, so reaching amount 0 counts as a cache hit.
3. **Experiment 2 (pseudo-polynomial scaling):** times the real
   `coin_change_dp` on `A = 2^8 … 2^18` with `COINS = [1,3,4]`, 7 repetitions
   each, and reports the median. Each row records `A`, its bit length, the
   number of DP states (`A + 1`), and the median runtime in ms. Timing includes
   reconstruction but not validation or CSV output.

## Output Files

| File | Contents | Reproducible? |
| --- | --- | --- |
| `part2c_experiment1.csv` | calls, distinct states, cache hits per target | Exact: counts are deterministic |
| `part2c_experiment2.csv` | A, bit length, states, median ms per target | States yes; times vary by machine and load |

Both files are written beside the script and overwritten on every run. The
write-up and interpretation are in `Memoization&Pseudo-Polynomial_Behavior.md`
and in the report.
