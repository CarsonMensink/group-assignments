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

## How to Run

From the project root, run:

```sh
python3 main.py
```

The main program will generate the test jobs through a helper function, so no input file is needed.

## Earliest Finish Time

Jobs are ordered based on smallest finish time first.
Ties are broken by the smaller index.
Running time is O(n log n)

## Earliest Start Time

Jobs are ordered based on smallest start time first.
Ties are broken by the smaller index.
Running time is O(n log n)

## Shortest Duration

Jobs are ordered based on shortest duration first.
Ties are broken by the smaller index.
Running time is O(n log n)

## Longest Duration

Jobs are ordered based on shortest duration first.
Ties are broken by the smaller index.
Running time is O(n log n)
