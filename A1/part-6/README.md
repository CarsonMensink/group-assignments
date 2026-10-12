# Part 6: Runtime Experiment

## Overview

This program tests the running times of our four greedy algorithms from Part 1: Earliest Finish Time, Earliest Start Time, Shortest Duration, and Longest Duration. It uses the shared algorithms from the root `algorithms` folder and the `Job` record from `jobs.py`.

## Language and Version

The project requires Python 3.10 or newer and uses only the standard library.

## How to Run

Use Python 3.10 or newer. No third-party packages are required.

From the `A1` folder, run this part directly:

```sh
python3 part-6/main.py
```

Or start the global menu:

```sh
python3 main.py
```

Enter `6` to run Part 6. After it finishes, the menu appears again; enter `q` to quit. The direct command runs only Part 6 and then exits.

## Expected Input Format

The benchmark generates its own random jobs, so no separate input file is needed.

Each job has a start time and finish time, where the finish time must be greater than the start time. The program generates instances containing 100, 1,000, 10,000, and 100,000 jobs.

Each generated job is stored with its start time, finish time, and original index so all four algorithms can use the same input records.

## Reproducing the Experiments

The program generates random intervals and runs all four algorithms 10 times for each input size. The same intervals are used for every algorithm at each input size to make the comparison fair.

The median execution time is calculated for each algorithm and saved to `part6_results.csv`.

The experiment can be repeated by running `python3 part-6/main.py` again. Execution times may vary depending on the computer being used.

## Randomness and Timing Details

Each run resets a local random generator to seed `4050`. For an input size `n`, job starts are integers chosen uniformly from `0` through `10n`; durations are integers from `1` through `100`. Finish time is start plus duration.

One job set is generated per size and reused for all four algorithms and all ten timed repetitions. Each algorithm receives one untimed warm-up per size. Timing uses `time.perf_counter()` and includes the algorithm's sorting and compatibility helper, but excludes input generation, printing, and CSV writing. The CSV stores the median in milliseconds for each size and algorithm. These repetitions measure timing variation on the same instance, not variation across ten different inputs.

All four implementations have O(n log n) worst-case time, including priority sorting and the shared helper's endpoint sorting and Fenwick-tree operations. See the engineering report for measured scaling; timing observations alone do not prove an asymptotic bound.
