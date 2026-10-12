### Optimal Solution

The optimal solution uses brute force to test every possible subset of jobs.

The solver accepts the same `Job` records used by the greedy algorithms. Each record stores its start time, finish time, and original index. It returns selected job indices without printing, so callers can choose how to display the result.

For each subset, every pair of jobs is checked to determine whether any two jobs overlap. If no jobs overlap, the subset is compatible.

The largest compatible subset found is saved as the optimal solution.

There are `2^n` possible subsets of `n` jobs. For each subset, up to `O(n^2)` pairs of jobs may need to be checked for compatibility.

**Total running time: `O(n^2 * 2^n)`**

Because this algorithm checks every possible subset, it is guaranteed to find an optimal solution, but it becomes impractical for large values of `n`.

## How to Run

Use Python 3.10 or newer. The exact solver is a shared module, not a separate menu option. From the `A1` folder, run `python3 main.py` and choose Part 3, 4, or 5. Each generates small instances and compares greedy results against this solver. Part 6 excludes the exact solver because exhaustive search is impractical at its input sizes. No input file or third-party package is needed.
