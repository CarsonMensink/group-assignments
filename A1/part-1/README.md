# Job Scheduling Greedy Algorithms

## Overview

This program compares multiple greedy algorithms for the interval scheduling problem.

Each job has a start time and finish time and is represented as a half-open interval:

`[start, finish)`

This means that a job finishing at time `t` is compatible with another job starting at time `t`.

The goal is to select the largest possible set of mutually compatible jobs.

The program implements:

- Earliest Finish Time
- Earliest Start Time
- Shortest Duration

## How to Run

The program uses an `input.txt` file containing the jobs.
To run do: python3 main.py < input.txt

The input format is:

n
start_time[0], start_time[1], ..., start_time[n]
finish_time[0], finish_time[1], ..., finish_time[n]

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