# Job Scheduling Greedy Algorithms

## Overview

This program compares multiple greedy algorithms for the interval scheduling problem.

Each job has a start time and finish time and is represented as a half-open interval:

`[start, finish)`

In the code, each interval is a `Job` record with `start`, `finish`, and its original `index`. The greedy algorithms accept a list of these records and return selected job indices without printing, so callers can choose how to display the results.

This means that a job finishing at time `t` is compatible with another job starting at time `t`.

The goal is to select the largest possible set of mutually compatible jobs.

The program implements:

- Earliest Finish Time
- Earliest Start Time
- Shortest Duration
- Longest Duration (our group's heuristic)

## How to Run

From the project root, run:

```sh
python3 main.py
```

The main program will generate the test jobs through a helper function, so no input file is needed.

## Earliest Finish Time

Jobs are ordered based on smallest finish time first.
Ties are broken by the smaller index.

Sorting costs O(n log n). The `select_forward_jobs` helper then makes one O(n) pass, accepting a job when its start is at least the last selected finish time.

**Total worst-case running time: O(n log n).**

## Earliest Start Time

Jobs are ordered based on smallest start time first.
Ties are broken by the smaller index.

Sorting costs O(n log n). The `select_forward_jobs` helper then makes one O(n) pass, accepting a job when its start is at least the last selected finish time.

**Total worst-case running time: O(n log n).**

## Shortest Duration

Jobs are ordered based on shortest duration first.
Ties are broken by the smaller index.

Sorting costs O(n log n). Because duration order can visit a later interval before an earlier one, `select_non_overlapping_jobs` checks each candidate against every already-selected job until an overlap is found. Compatible jobs may occur before or after the selected intervals.

If all n jobs are compatible, the helper performs 0 + 1 + ... + (n - 1) = n(n - 1)/2 comparisons, giving O(n²) selection time. Returning the selected indices adds O(n).

**Total worst-case running time: O(n log n + n²) = O(n²).**

## Longest Duration

Jobs are ordered based on longest duration first.
Ties are broken by the smaller index.

Sorting costs O(n log n). This algorithm uses the same `select_non_overlapping_jobs` helper as Shortest Duration because duration order does not guarantee chronological order. Checking candidates against already-selected jobs costs O(n²) in the worst case, and returning selected indices adds O(n).

**Total worst-case running time: O(n log n + n²) = O(n²).**

## Runtime Summary

Here, n is the number of input jobs. These bounds describe the current implementations.

| Algorithm | Sorting | Selection | Total worst-case time |
| --- | --- | --- | --- |
| Earliest Finish Time | O(n log n) | O(n) | O(n log n) |
| Earliest Start Time | O(n log n) | O(n) | O(n log n) |
| Shortest Duration | O(n log n) | O(n²) | O(n²) |
| Longest Duration | O(n log n) | O(n²) | O(n²) |
