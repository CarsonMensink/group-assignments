# Part 2B: Exact Solver Validation & Greedy Counterexample Search

This project validates multiple coin-change solvers and checks whether the largest-first greedy strategy can fail.

## What it does
- Compares three exact solvers:
  - naive recursion
  - top-down memoization
  - bottom-up dynamic programming
- Checks all solver outputs with an independent validator
- Uses the DP solution as ground truth to search for greedy counterexamples
- Writes discovered counterexamples to `greedy_counterexamples.csv`

## Run it
Requires Python 3.10 or newer. No third-party packages are needed.

From the repository root, run:

```bash
python3 A2/part-2/2b/main.py
```

Or run `python3 main.py` from `A2/part-2/2b/`. Both commands validate the
exact solvers, search for greedy failures, assert the required sanity check,
and regenerate `A2/part-2/2b/greedy_counterexamples.csv`. The output path is
relative to the script, so it does not depend on the current working directory.
Run with normal Python; `python3 -O` disables the assertions used for validation.

## Included checks
- **12 hand-checkable cases:** target zero with and without denomination 1,
  impossible targets, single-denomination cases, greedy traps, and multiple
  optimal solutions (`D=[2,3,4], A=6`, where `3+3` and `2+4` both use two coins).
- **150 randomized cases:** local random seed **4050**, 2–5 denominations,
  denomination 1 always present, other denominations sampled without replacement
  from 2–14, and target amounts sampled from 0–22. The target ceiling keeps
  naive recursion practical; the hand cases include targets up to 30.
- Every case compares the optimal counts from naive recursion, top-down
  memoization, and bottom-up DP using the shared Part 2A implementations.
  Hand cases also check an independently hand-counted expected answer.
- Every exact solver's returned list is checked independently for sum, count,
  and allowed denominations. `(-1, None)` is checked for failure shape;
  hand-counted impossible cases and solver comparisons check the failure claim.
  Equally good reconstructed lists need not be identical.
- **Systematic search:** all 91 systems `[1,c2,c3]` with `1 < c2 < c3 <= 15`,
  each at targets 1–25 (2,275 instances). Both greedy and DP lists are validated.
  Only feasible greedy results using more coins than DP count as counterexamples.

These finite tests validate the tested implementations and inputs; they do not
prove correctness for all possible instances.

## Expected output
- pass/fail results for the curated and randomized tests
- a sanity check for the classic greedy trap `D = {1, 3, 4}, A = 6`
- summary of any counterexamples found
- CSV export of the discovered examples

The structural explanation below accompanies the results; it is not printed by
the program.

The current search finds **197** suboptimal greedy instances. The CSV exports
the required sanity case first and then the first two examples with different
denomination systems, in deterministic search order:

| Denominations | Target | Greedy coins | Optimal coins | Extra coins |
|---|---:|---|---|---:|
| `[1,3,4]` | 6 | `[4,1,1]` (3) | `[3,3]` (2) | 1 |
| `[1,4,5]` | 8 | `[5,1,1,1]` (4) | `[4,4]` (2) | 2 |
| `[1,4,6]` | 8 | `[6,1,1]` (3) | `[4,4]` (2) | 1 |

The runner fails if the required sanity case is absent, its greedy solution is
not `[4,1,1]` with count 3, its optimal count is not 2, or fewer than three
distinct systems are available for export. The CSV records denominations,
target, both counts and reconstructed lists, and the extra coins greedy used.

## Example structural explanation
For `D = {1, 3, 4}` and `A = 6`, taking 4 leaves a remainder of 2.
That remainder is smaller than every denomination except 1, so greedy must
finish with `1+1`, using three coins in total. Choosing 3 first instead leaves
another 3, giving `3+3` in two coins. One coin cannot form 6, so two coins is
optimal. The largest local choice prevents the better combination by leaving
a remainder too small to use the middle denomination.

## Notes
The program generates its own test data; no external input file is required.
