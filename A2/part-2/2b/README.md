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

From the project folder, run:

```bash
python3 main.py
```

## Included checks
- 12 hand-checkable test cases
- 150 randomized validation cases
- systematic search over 3-coin systems to find greedy suboptimal solutions

## Expected output
- pass/fail results for the curated and randomized tests
- a sanity check for the classic greedy trap `D = {1, 3, 4}, A = 6`
- summary of any counterexamples found
- CSV export of the discovered examples
- an explanation of at least one counterexample showing why the largest-coin local choice can block a better global combination

## Example structural explanation
For the system `D = {1, 3, 4}` and target `A = 6`, the greedy rule picks the largest feasible coin first, choosing `4`, then `1`, then `1`, for a total of 3 coins. However, the globally optimal combination is `3 + 3`, using only 2 coins. Structurally, the large coin makes the remainder `2`, which cannot be completed optimally without wasting a large denomination early; choosing `3` instead preserves a remainder that is itself exactly representable by a second `3`, leading to a smaller total coin count. This shows that a locally largest coin can prevent a better global arrangement even when the remainder is still feasible.

## Notes
The program generates its own test data; no external input file is required.
