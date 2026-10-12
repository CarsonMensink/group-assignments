# Part 4: Test the Correct Greedy Algorithm

## Overview

Part 4 of the [assignment](../CMP_SC_4050_FS2026_GEA1%20%281%29.pdf) asks us to compare the number of jobs selected by Earliest Finish Time with the optimal number, `OPT(I)`, on at least 100 randomly generated instances from multiple distributions. No input file is needed; each job is a half-open interval `[start, finish)`, so a job may start when another finishes.

## How to Run

Use Python 3.10 or newer. No third-party packages are required.

From the `A1` folder, run this part directly:

```sh
python3 part-4/main.py
```

Or start the global menu:

```sh
python3 main.py
```

Enter `4` to run Part 4. After it finishes, the menu appears again; enter `q` to quit. The direct command runs only Part 4 and then exits.

## Test Generation

`generate_tests` in `utils.py` creates 100 reproducible cases using random seed `2026`. Each case has 15 jobs. The cases are divided evenly among sparse intervals, heavily overlapping intervals, varied lengths, and clustered start times.

`main.py` runs Earliest Finish Time and the exact solver on every case. `compare_test` records the intervals, both sets of selected job indices, both solution sizes, and whether the sizes match. All 100 cases are processed even if one does not match.

## Results

The terminal shows a Part 4 title, the overall match ratio, and a message that the CSV was saved. The checked run matched OPT on 100/100 instances (100%). Each run overwrites [part4_validation_results.csv](part4_validation_results.csv) with one row per case. The interval and selected-job lists are stored as JSON within their CSV cells so each case can be inspected later.

The match ratio is `(# cases where Earliest Finish matched OPT) / 100`. Agreement across these tests helps validate the implementation, but it does not prove that Earliest Finish is always optimal.
