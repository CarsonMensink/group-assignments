# Part 6: Runtime Experiment

## Overview

This program tests the running times of our four greedy algorithms from Part 1: Earliest Finish Time, Earliest Start Time, Shortest Duration, and Longest Duration.

## Language and Version

The program is written in Python 3.

## How to Run

The program uses the greedy algorithms from the `part-1` folder.

To run the experiment, open a terminal in the `part-6` folder and enter:

```
python benchmark_part6.py
```

## Expected Input Format

The benchmark generates its own random jobs, so no separate input file is needed.

Each job has a start time and finish time, where the finish time must be greater than the start time. The program generates instances containing 100, 1,000, 10,000, and 100,000 jobs.

## Reproducing the Experiments

The program generates random intervals and runs all four algorithms 10 times for each input size. The same intervals are used for every algorithm at each input size to make the comparison fair.

The median execution time is calculated for each algorithm and saved to `part6_results.csv`.

The experiment can be repeated by running `benchmark_part6.py` again. Execution times may vary depending on the computer being used.
