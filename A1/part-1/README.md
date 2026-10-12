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

Use Python 3.10 or newer. These shared algorithms are exercised by Parts 3–6; there is no separate Part 1 menu option. From the `A1` folder, run `python3 main.py` and choose Part 3 for counterexamples, Part 4 for Earliest Finish validation, Part 5 for solution quality, or Part 6 for runtime measurements. No input file or third-party package is needed.

## Earliest Finish Time

Jobs are ordered based on smallest finish time first.
Ties are broken by the smaller index.

Sorting costs O(n log n). The shared `select_compatible_jobs` helper uses Fenwick trees to check compatibility and record accepted jobs in O(n log n) total time.

**Total worst-case running time: O(n log n).**

## Earliest Start Time

Jobs are ordered based on smallest start time first.
Ties are broken by the smaller index.

Sorting costs O(n log n). The shared `select_compatible_jobs` helper uses Fenwick trees to check compatibility and record accepted jobs in O(n log n) total time.

**Total worst-case running time: O(n log n).**

## Shortest Duration

Jobs are ordered based on shortest duration first.
Ties are broken by the smaller index.

Sorting costs O(n log n). The shared `select_compatible_jobs` helper checks each candidate in O(log n), including candidates that fit before, after, or between selected intervals. Its total cost is O(n log n).

**Total worst-case running time: O(n log n).**

## Longest Duration

Jobs are ordered based on longest duration first.
Ties are broken by the smaller index.

Sorting costs O(n log n). This algorithm uses the same `select_compatible_jobs` helper as the other strategies, with O(log n) overlap checks and O(n log n) total selection time.

**Total worst-case running time: O(n log n).**

## Shared Compatibility Helper

The helper compresses the input endpoints into ordered positions in O(n log n) time. Two Fenwick trees count starts and finishes of selected jobs. For a candidate, the overlap count is:

`selected starts < candidate.finish` minus `selected finishes <= candidate.start`.

For valid intervals (`start < finish`), a zero count means the candidate overlaps no selected job. The strict start boundary and inclusive finish boundary allow touching endpoints. Each query and accepted-endpoint update takes O(log n), and all helper storage uses O(n) space. Jobs are still considered in the caller's priority order.

## Runtime Summary

Here, n is the number of input jobs. These bounds describe the current implementations.

| Algorithm | Sorting | Selection | Total worst-case time |
| --- | --- | --- | --- |
| Earliest Finish Time | O(n log n) | O(n log n) | O(n log n) |
| Earliest Start Time | O(n log n) | O(n log n) | O(n log n) |
| Shortest Duration | O(n log n) | O(n log n) | O(n log n) |
| Longest Duration | O(n log n) | O(n log n) | O(n log n) |
