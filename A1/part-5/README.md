# Part 5: Compare Greedy Algorithms

## Overview

The experiment compares all four greedy algorithms against the exact solver on 120 reproducible instances and writes detailed and summary CSV files in this folder.

## How to Run

Use Python 3.10 or newer. No third-party packages are required.

From the `A1` folder, run this part directly:

```sh
python3 part-5/main.py
```

Or start the global menu:

```sh
python3 main.py
```

Enter `5` to run Part 5. After it finishes, the menu appears again; enter `q` to quit. The direct command runs only Part 5 and then exits.

## Expected Input Format

No input file is needed. Every instance contains 6–12 jobs. Solvers receive indexed `Job` records for half-open intervals.

## Reproducing the Experiments

The experiment resets its local seed to `4050` and generates 120 instances, cycling through four distributions so each receives 30 cases:

| Distribution | Start times | Durations |
| --- | --- | --- |
| Sparse | Integers 0–100 | Integers 1–4 |
| Overlapping | Integers 0–10 | Integers 8–20 |
| Varied lengths | Integers 0–40 | One of 1, 2, 3, 5, 10, 20, 30 |
| Clustered | A center from 10, 30, 50 plus an integer offset from -3 to 3 | Integers 1–15 |

All four heuristics and the exact solver receive the same jobs for each instance.

## Results

Quality is `selected job count / optimal job count`. A value of 1 is optimal. For each heuristic, the output reports the percentage of optimal instances, average quality, and the lowest observed quality with a complete worst-case example. When worst-quality values tie, the first instance is retained.

- `comparison_results.csv`: one row per instance and heuristic (480 rows), including inputs, selections, counts, and quality.
- `comparison_summary.csv`: one row per heuristic, including aggregate metrics and its worst observed instance.

Both files are overwritten on rerun. See the engineering report for interpretation of the measured results.
