# Part 3: Automatically Find Counterexamples

## Overview

Find failures of Earliest Start, Shortest Duration, and Longest Duration, using the exact solver as the reference.

## How to Run

Use Python 3.10 or newer. No third-party packages are required.

From the `A1` folder, run this part directly:

```sh
python3 part-3/main.py
```

Or start the global menu:

```sh
python3 main.py
```

Enter `3` to run Part 3. After it finishes, the menu appears again; enter `q` to quit. The direct command runs only Part 3 and then exits.

## Expected Input Format

No input file is needed. Search instances have 4–10 jobs, starts chosen uniformly from integers 0–20, and durations from integers 1–8. Solvers receive indexed `Job` records representing half-open intervals.

## Reproducing the Experiments

Every run resets the random seed to `4050`. First, the required Earliest Start example must select 1 job against OPT's 4, and the required Shortest Duration example must select 1 against OPT's 2. A failed sanity check stops the run.

The search then tries up to 5,000 instances per heuristic and stops at its first counterexample. Finally, Earliest Finish is compared against OPT on 100 generated instances with 1–10 jobs and the same start/duration ranges. The search remains automated; it does not use Part 4's fixed batch generator.

## Output and Interpretation

For each discovered counterexample, the terminal shows all input intervals, both selections, both solution sizes, the search attempt count, and an indexed interval timeline. `counterexamples.csv` contains one row per heuristic with its name, seed, whether a counterexample was found, attempt count, input intervals, both selections, and both solution sizes. Lists are stored as JSON text inside CSV cells; an interval’s position is its zero-based job index. If a search finds no counterexample, `Counterexample_Found` is `False` and the evidence fields are blank. Each run overwrites this file.

A counterexample proves that a heuristic is not always optimal. Finding none within a finite search does not prove optimality. Likewise, agreement in the Earliest Finish validation is evidence about the implementation, not a correctness proof.
