# Engineering Report: Interval Scheduling

**Technical draft.** The group's personal response in Part 7 and final 4–6-page layout remain to be completed before submission. Results below were regenerated from the current code; input indices are zero-based.

## Problem and algorithms (Parts 1 and 2)

The objective is to maximize the number of mutually compatible jobs. Intervals are half-open, so a job ending at time t can be followed by a job starting at t. All algorithms return selected input indices, allowing the experiment to inspect actual schedules as well as their sizes.

| Strategy | Priority | Tie-breaking | Worst-case time |
| --- | --- | --- | --- |
| Earliest Finish | Increasing finish time | Smaller input index | O(n log n) |
| Earliest Start | Increasing start time | Smaller input index | O(n log n) |
| Shortest Duration | Increasing finish minus start | Smaller input index | O(n log n) |
| Longest Duration | Decreasing finish minus start | Smaller input index | O(n log n) |

Longest Duration is the group's additional rule. Its priority differs from all three required rules, but choosing a long interval offers no guarantee of scheduling the largest number of jobs.

Each heuristic sorts the input and uses the same compatibility helper. The helper compresses endpoints into sorted positions and uses two Fenwick trees to count conflicts with accepted intervals. It accepts a candidate only when its overlap count is zero. Compatible intervals can be accepted before, after, or between earlier selections; an interval is not rejected merely because it occurs earlier in time than an already accepted job. The strict/inclusive boundaries preserve the half-open convention. Priority sorting, endpoint sorting, and O(log n) queries or updates yield O(n log n) total time and O(n) auxiliary space.

The exact solver enumerates every subset and checks every pair within each candidate subset. Because every feasible selection is among these subsets, keeping a largest feasible subset yields an optimum. Its worst-case time is O(n² 2ⁿ). This exponential growth makes it appropriate for the small experiments, but unsuitable for the benchmark's large input sizes.

## Methodology and reproducibility

The run used Python 3.14.6 on macOS-14.5-arm64-arm-64bit-Mach-O. The programs require only the Python standard library. Each experiment resets its seed, so running another menu choice first does not change its generated instances. Part 3 uses seed 4050, Part 4 uses 2026, and Parts 5 and 6 use 4050. Generator ranges and commands are documented in each part's README.

Both required sanity checks passed: Earliest Start selected 1 job where OPT selected 4, and Shortest Duration selected 1 where OPT selected 2. Part 3 runs these checks before searching. We exercised both standalone commands and the global menu; deterministic result files for Parts 3–5 were byte-identical between those runs. These are automated checks performed during the Codex-assisted update; the group must independently review their correctness before submission.

## Automatically discovered counterexamples (Part 3)

The search generates 4–10 jobs per instance, with integer starts from 0–20 and durations from 1–8. It searches separately for each incorrect heuristic, stopping at its first failure or after 5,000 attempts. The following examples come from `part-3/counterexamples.csv`, rather than manual construction.
### Earliest Start

Found on attempt 4. Complete input: 0: [16, 22); 1: [9, 11); 2: [14, 18); 3: [13, 20); 4: [0, 2); 5: [0, 1); 6: [13, 14); 7: [19, 21).

Heuristic selection: [4, 1, 3] (3 jobs). One optimal selection: [1, 2, 4, 6, 7] (5 jobs).
### Shortest Duration

Found on attempt 178. Complete input: 0: [13, 18); 1: [6, 13); 2: [4, 8); 3: [19, 23); 4: [11, 19); 5: [1, 5).

Heuristic selection: [2, 3, 0] (3 jobs). One optimal selection: [0, 1, 3, 5] (4 jobs).
### Longest Duration

Found on attempt 1. Complete input: 0: [9, 14); 1: [2, 10); 2: [14, 15); 3: [2, 8); 4: [18, 23); 5: [11, 16).

Heuristic selection: [1, 4, 5] (3 jobs). One optimal selection: [0, 2, 3, 4] (4 jobs).
Earliest Start commits to [13, 20), blocking several shorter jobs later in that region. Shortest Duration selects [4, 8), which overlaps both [1, 5) and [6, 13), even though those two can coexist. Longest Duration commits to [2, 10) and later [11, 16), excluding the compatible chain [2, 8), [9, 14), [14, 15).

The following timeline visualizes the automatically found Shortest Duration example. Each dash represents one occupied time unit; all intervals are half-open. `G` marks a greedy selection and `O` an optimal selection.

```text
Time     0    5    10   15   20
0 GO                  ----- [13, 18)
1  O           ------- [6, 13)
2 G          ---- [4, 8)
3 GO                        ---- [19, 23)
4                   -------- [11, 19)
5  O      ---- [1, 5)
```

A single valid counterexample disproves an always-optimal claim. Failure to find a counterexample within a finite search does not establish optimality. Part 3 also compared Earliest Finish with OPT on 100 additional random instances; all passed.

## Earliest Finish validation (Part 4)

Part 4 generated 100 instances of 15 jobs each, divided evenly among sparse, heavily overlapping, varied-length, and clustered-start distributions. Earliest Finish matched OPT on **100/100 instances (100%)**. Inputs, selections, sizes, and matches are saved in `part-4/part4_validation_results.csv`.

Agreement is evidence that the implementation handles these cases correctly. The general optimality of Earliest Finish requires a mathematical argument: choosing an earliest-finishing job leaves at least as much remaining time as the first job in an optimal schedule, allowing an exchange argument to continue on the remaining compatible jobs. The experiments themselves do not establish this for all inputs.

## Solution quality (Part 5)

The comparison uses 120 instances of 6–12 jobs, with 30 per distribution. All heuristics receive the same inputs, and OPT is computed once per instance. Quality is the selected count divided by OPT. The average is the arithmetic mean of per-instance ratios.

| Heuristic | Optimal instances | Optimal percentage | Average quality | Worst quality |
| --- | --- | --- | --- | --- |
| Earliest Finish | 120/120 | 100.00% | 1.0000 | 1.0000 |
| Earliest Start | 85/120 | 70.83% | 0.9100 | 0.2857 |
| Shortest Duration | 116/120 | 96.67% | 0.9897 | 0.5000 |
| Longest Duration | 81/120 | 67.50% | 0.8860 | 0.2857 |

Earliest Finish was optimal across all four distributions. Earliest Start was optimal on all 30 sparse cases, but only 11/30 varied-length cases and 16/30 clustered cases. Starting early can commit the schedule to a long blocking interval. Longest Duration performed especially poorly on varied lengths (9/30 optimal), where a long interval can exclude a chain of short jobs.

Shortest Duration was strongest among the incorrect rules in this experiment: it was optimal on all sparse cases and missed optimality only four times overall. Its good aggregate performance does not remove its failure mode: a short interval can sit across the boundary between two compatible alternatives. This occurs in its worst overlapping instance below. These observations are specific to the generated sample and do not establish universal rankings.

### Worst observed instances

All jobs are listed as `(index, start, finish)`. Tied worst qualities retain the first encountered instance. Earliest Finish's worst observed quality is still 1, so its example is not a failure.

**Earliest Finish — instance 1 (sparse).** Input: `[(0, 63, 66), (1, 2, 6), (2, 88, 89), (3, 33, 36), (4, 64, 68), (5, 5, 8), (6, 50, 54), (7, 77, 78), (8, 43, 45)]`. Heuristic: `[1, 3, 8, 6, 0, 7, 2]` (7 jobs). OPT: `[0, 1, 2, 3, 6, 7, 8]` (7 jobs).

**Earliest Start — instance 39 (varied_lengths).** Input: `[(0, 26, 28), (1, 10, 13), (2, 16, 46), (3, 36, 38), (4, 31, 33), (5, 21, 24), (6, 27, 57), (7, 12, 17), (8, 33, 35), (9, 18, 19), (10, 20, 50)]`. Heuristic: `[1, 2]` (2 jobs). OPT: `[0, 1, 3, 4, 5, 8, 9]` (7 jobs).

**Shortest Duration — instance 46 (overlapping).** Input: `[(0, 3, 15), (1, 7, 20), (2, 6, 14), (3, 9, 22), (4, 10, 19), (5, 4, 16), (6, 0, 9)]`. Heuristic: `[2]` (1 jobs). OPT: `[3, 6]` (2 jobs).

**Longest Duration — instance 39 (varied_lengths).** Input: `[(0, 26, 28), (1, 10, 13), (2, 16, 46), (3, 36, 38), (4, 31, 33), (5, 21, 24), (6, 27, 57), (7, 12, 17), (8, 33, 35), (9, 18, 19), (10, 20, 50)]`. Heuristic: `[2, 1]` (2 jobs). OPT: `[0, 1, 3, 4, 5, 8, 9]` (7 jobs).

The complete per-instance evidence and aggregate results are in `part-5/comparison_results.csv` and `part-5/comparison_summary.csv`.

## Runtime experiment (Part 6)

Only greedy algorithms are benchmarked. For each size, one random job set is reused across every heuristic and repetition. Starts range from 0 to 10n and durations from 1 to 100. Each algorithm receives an untimed warm-up followed by ten timed calls; the median is reported in milliseconds. Timings include priority sorting and the compatibility helper, and exclude generation, output, and CSV writing.

| Jobs | Earliest Finish | Earliest Start | Shortest Duration | Longest Duration |
| --- | --- | --- | --- | --- |
| 100 | 0.117 | 0.109 | 0.117 | 0.110 |
| 1,000 | 1.504 | 1.414 | 1.550 | 1.474 |
| 10,000 | 19.936 | 18.615 | 21.295 | 20.164 |
| 100,000 | 268.023 | 252.886 | 313.271 | 300.779 |

For the last tenfold increase in n, measured times increased by 13.4–14.9 times. The n log n term increases by about 12.5 times from 10,000 to 100,000. The measurements are broadly consistent with superlinear sorting-and-tree costs, with differences attributable to constants, memory behavior, and system conditions. They do not prove an asymptotic bound.

The shared helper explains why runtimes are similar in scale. Different priority orders still incur different sorting costs and accept different numbers of jobs, affecting tree updates. Earliest Finish could be implemented with a simpler linear scan after sorting, but these measurements describe the shared-helper implementation actually used here. One generated instance per size limits conclusions about timing across input distributions. The machine-readable measurements are in `part-6/part6_results.csv`.

## Engineering reflection (Part 7)

1. **Which incorrect heuristic seemed most convincing before testing?** Pending the group's own answer and reason. This personal judgment cannot be reconstructed from the measurements. Shortest Duration's strong measured performance is evidence about this sample, not evidence of the group's prior belief.
2. **What did the counterexample reveal?** Local priority does not measure how many future choices are lost. The automatically found Shortest Duration example selects [4, 8), sacrificing both [1, 5) and [6, 13). Earliest Start and Longest Duration similarly select intervals that block longer compatible chains.
3. **What did the exact solver contribute?** It provides an independently defined optimum on small instances, making it possible to label a heuristic failure, calculate quality ratios, and show a concrete better schedule. Its exponential cost also determines the practical input sizes for validation.
4. **How does experimental validation differ from proof?** Tests can expose a failure and increase confidence in an implementation on sampled inputs. They cannot establish a universal claim over all interval sets. A correctness proof supplies that general argument; tests also remain necessary to catch deviations between a proven algorithm and its implementation.

## Conclusions and submission checks

Earliest Finish matched OPT throughout the measured instances. Each alternative had an automatically discovered counterexample, even though Shortest Duration often matched OPT. All four current implementations have the same worst-case asymptotic runtime, while their solution quality differs. The benchmark is consistent with the implementation's sorting and Fenwick-tree costs within the limits of the measurement setup.

Before submission, the group must fill in its personal reflection and member contributions, confirm all AI usage, independently validate the technical claims, and lay out this draft as an approximately 4–6-page report. See `CONTRIBUTIONS.md` and `AI_USE.md`.
