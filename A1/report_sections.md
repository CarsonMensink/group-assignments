# Group Algorithm Engineering Assignment 1: Report Sections (Draft)

Authors: Connor Souders, Carson Mensink, Alexis Paten, Chris Crowder, Deniz Kavzak Ufuktepe
CMP_SC 4050, 2026 October 12

Items in square brackets need a team decision or a fact only the team can confirm.

---

## Algorithm Descriptions

All four strategies share one selection rule. Each job is a half-open interval `[s, f)`, so a job finishing at time `t` is compatible with a job starting at time `t`. After the jobs are put in a chosen order, we scan them once. We keep a job when its start is at or after the finish of the last kept job, and we record its original index. This scan takes `O(n)` time. Each strategy differs only in the order used for the scan, so the only thing that changes between algorithms is the sort key. Every strategy breaks ties by the smaller original index, which makes all four deterministic and reproducible.

### A. Earliest Finish Time (EFT)

EFT sorts the jobs by finish time, smallest first, with ties broken by index. It is the algorithm presented in class. Its key property is that finishing as early as possible leaves the largest remaining time window for later jobs. A standard exchange argument shows that EFT always produces an optimal schedule: take any optimal schedule, and replace its first job with EFT's first job. The EFT job finishes no later, so the replacement remains feasible and no job is lost. Repeating this argument on the remaining jobs gives optimality.

- Ordering: non-decreasing finish time `f_j`, ties by index.
- Running time: `O(n log n)`, dominated by the sort; the scan is `O(n)`.

### B. Earliest Start Time (EST)

EST sorts the jobs by start time, smallest first, with ties broken by index. The intuition is "start working as soon as possible," but this ignores how long a job runs. A job that starts first may occupy a long stretch of time and block many shorter jobs that come after it. This is the failure shown in Sanity Test 1.

- Ordering: non-decreasing start time `s_j`, ties by index.
- Running time: `O(n log n)`.

### C. Shortest Duration (SD)

SD sorts the jobs by duration `f_j - s_j`, smallest first, with ties broken by index. The intuition is that short jobs use little time. The rule fails when a short job sits across the boundary between two other jobs that are compatible with each other, so picking it blocks both. This is the failure shown in Sanity Test 2.

- Ordering: non-decreasing `f_j - s_j`, ties by index.
- Running time: `O(n log n)`.

### D. Group Heuristic: Longest Duration (LD)

[Team to confirm that this is the heuristic the group wants to submit as "D." LD is a valid choice under the assignment rules because it is not one of A to C under a different name.]

LD sorts the jobs by duration, largest first, with ties broken by index. The intuition is to fill the schedule with the largest blocks of time, and then fit smaller jobs into what is left. The rule is a poor one. A long job tends to overlap with many other jobs, so selecting it blocks many potential choices at once.

- Ordering: non-increasing `f_j - s_j`, ties by index.
- Running time: `O(n log n)`.

Note for the code: `part-1/README.md` currently describes Longest Duration as "ordered based on shortest duration first." This is incorrect, since the code sorts by longest duration first. The README should be corrected before submission.

---

## Counterexamples

A counterexample is one input on which a greedy strategy returns fewer jobs than the optimum. Each example below was checked by running the current code in `A1/algorithms/` and `A1/algorithms/optimal_algorithm.py`. The job indices are the original input indices.

### Earliest Start: Sanity Test 1 (required)

| Input intervals | Earliest Start selects | Greedy size | Optimal selects | OPT size |
|---|---|---|---|---|
| A=(0,10), B=(1,2), C=(2,3), D=(3,4), E=(4,5) | A | 1 | B, C, D, E | 4 |

EST picks A because it starts first at time 0. A then covers the whole range `[0, 10)`, so none of B through E can be selected. This gives `|EST(I)| = 1` and `OPT(I) = 4`.

A second counterexample, found on a random 11-job instance from Part 5: EST selects 2 jobs and the optimum selects 7.

### Shortest Duration: Sanity Test 2 (required)

| Input intervals | SD selects | Greedy size | Optimal selects | OPT size |
|---|---|---|---|---|
| A=(2,4), B=(0,3), C=(3,6) | A | 1 | B, C | 2 |

SD picks A because it has the smallest duration (2). A overlaps both B and C, so the algorithm stops after one job. B and C are compatible with each other, since B finishes at 3 and C starts at 3. This gives `|SD(I)| = 1` and `OPT(I) = 2`.

A second, clustered counterexample from Part 5 (8 jobs): SD selects 1 job and the optimum selects 3.

Timeline for Sanity Test 2 (`#` marks the slots a job covers; the optimum is B and C):

```
slot:  0 1 2 3 4 5
A      . . # # . .    <- chosen by SD
B      # # # . . .    <- optimal
C      . . . # # #    <- optimal
```

### Longest Duration (group heuristic): Part 5 Instance 3

| Input intervals (index: [s, f)) | LD selects | Greedy size | Optimal selects | OPT size |
|---|---|---|---|---|
| 0:[25,55), 1:[19,39), 2:[32,42), 3:[36,41), 4:[28,38), 5:[35,55), 6:[18,21) | 0 | 1 | 0, 6 | 2 |

LD picks job 0 because it is the longest (length 30). Job 0 overlaps every other job except job 6, which is short and finishes at 21 before job 0 starts at 25. Choosing job 0 therefore rules out everything except job 6, and the rule stops at one job. The optimum takes jobs 0 and 6, which are compatible, so it gets two. [Team to double-check this row against `part-5/comparison_results.csv`, instance 3.]

### Finding a counterexample versus proving optimality

Finding a counterexample proves that a heuristic is not always optimal, because one failing input is enough. It does not prove that the heuristic is optimal on all other inputs, and it does not say how often the heuristic fails. The absence of a counterexample is also not a proof. Our random search and the Part 4 tests cover only a finite set of random instances, so they can support the conclusion that EFT is correct but cannot establish it. The only thing that proves EFT's correctness is the exchange argument above.

---

## Exact Solver

The exact solver in `A1/algorithms/optimal_algorithm.py` is a brute-force search. It enumerates every subset of the `n` jobs, in increasing size order, using `itertools.combinations`. For each subset it checks every pair of jobs using the half-open overlap test `job1.start < job2.finish and job2.start < job1.finish`. A subset is kept when no pair overlaps and it is larger than the best subset found so far.

Because every subset is examined, the solver always returns an optimal solution. This makes it a trustworthy oracle for the experiments.

**Running time:** there are `2^n` subsets. For a subset of size `k`, the pairwise check takes `O(k^2)` time, so the total running time is `O(n^2 * 2^n)`. This matches `part-2/README.md`. The count doubles with each added job, so the solver is only practical for small `n`. We used it with `n = 15` (Part 4) and `n` between 6 and 12 (Part 5), which keeps each instance feasible.

---

## Experimental Methodology

All experiments are run from the project root with `python3 main.py` (Part 4) or the equivalent scripts for Parts 5 and 6. Random generation uses fixed seeds, so the results are reproducible.

### Part 4: Validation of Earliest Finish

`utils.generate_tests` produces 100 instances with seed `2026`. Each instance has 15 jobs. The instances rotate evenly through four distributions, giving 25 instances per type:

- **Sparse:** short durations (1 to 5), starts spread over `[100, 500]`.
- **Heavily overlapping:** starts in `[100, 120]`, durations 50 to 100.
- **Varied lengths:** starts in `[100, 300]`, durations that are either short (1 to 3) or long (50 to 100).
- **Clustered starts:** starts within 5 of the milestones 100, 200, or 300, durations 10 to 30.

| Distribution | Earliest Finish matched OPT |
|---|---|
| Sparse | 25 / 25 |
| Heavily overlapping | 25 / 25 |
| Varied lengths | 25 / 25 |
| Clustered starts | 25 / 25 |
| **Total** | **100 / 100 (100%)** |

The full per-instance record is in `part-4/part4_validation_results.csv`. Each row includes the intervals, both selections, and both sizes.

### Part 5: Comparison of the Four Heuristics

`part-5/comparisons.py` generates 120 instances with seed `4050`, 30 for each of four types: sparse, overlapping, varied lengths, and clustered. Each instance has between 6 and 12 jobs, so the exact solver can be applied to each one. For each heuristic `H` we compute `|H(I)| / OPT(I)`, and we record the worst instance.

| Heuristic | % instances optimal | Average `|H|/OPT` | Worst `|H|/OPT` |
|---|---|---|---|
| Earliest Finish | 100.00% | 1.0000 | 1.0000 |
| Earliest Start | 70.83% | 0.9100 | 0.2857 |
| Shortest Duration | 27.50% | 0.6065 | 0.1111 |
| Longest Duration | 22.50% | 0.5061 | 0.1111 |

Source: `part-5/comparison_summary.csv`. Per-heuristic detail is in `part-5/comparison_results.csv`.

**What misleads each heuristic.**

- **Earliest Start** is usually reasonable on random instances (71% optimal) because the early-starting job is often short. Its failures come from a single long interval that starts early and covers many later jobs. The worst case we observed (quality 0.2857) is of this type: one early long job blocks most of the schedule.
- **Shortest Duration** fails when a short interval lies across the gap between two compatible intervals. This is common when intervals are spread out and short intervals sit on the boundaries of longer ones. Its worst case (quality 0.1111) comes from a sparse instance.
- **Longest Duration** is the weakest heuristic (22.5% optimal). Long intervals overlap many others, so selecting one early removes many options. Its worst case (quality 0.1111) also comes from a sparse instance, where one long job blocks many short, compatible jobs.

**Caveat.** `part-5/comparisons.py` currently fails to run. It imports from `part-1/` and `part-2/` paths that were removed in the refactor, so the CSVs above were produced before that change. The script needs to be updated to import from `algorithms/` and `algorithms/optimal_algorithm.py` before the results can be reproduced from the final code.

### Part 6: Runtime Experiment

`part-6/benchmark_part6.py` times each greedy algorithm on random inputs of size `n = 100, 1,000, 10,000, 100,000`. The generator uses seed `4050`, and every algorithm is run on the same input at each size. Each algorithm gets one warm-up run, followed by 10 timed runs. The reported value is the median, in milliseconds.

| n | Earliest Finish | Earliest Start | Shortest Duration | Longest Duration |
|---|---|---|---|---|
| 100 | 0.016 | 0.016 | 0.017 | 0.018 |
| 1,000 | 0.279 | 0.248 | 0.233 | 0.263 |
| 10,000 | 5.839 | 6.175 | 5.903 | 4.816 |
| 100,000 | 130.25 | 115.83 | 103.87 | 116.36 |

Source: `part-6/part6_results.csv`.

**Interpretation.** Each step up in `n` by a factor of 10 multiplies the time by roughly 16 to 25. This is consistent with `O(n log n)`, since `log n` grows only slowly over this range. A linear `O(n)` algorithm would show a factor closer to 10. The sort is the dominant cost: every algorithm sorts `n` jobs with Python's `sorted`, which is `O(n log n)`, while the selection scan is only `O(n)`. Since all four algorithms share the same scan and sort structure, their times are similar. Differences between algorithms of up to about 25% at the same `n` (for example, Earliest Finish versus Shortest Duration at `n = 100,000`) are not reliable as evidence that one algorithm is faster. All four share the same sort and scan, so their costs should be similar, and single-machine timing noise can account for this gap.

These four sizes are not enough to prove an asymptotic bound. They show that the measurements agree with the analysis, but cannot exclude other growth rates over a wider range of `n`.

---

## Discussion and Conclusion

### Engineering Reflection

**1. Which incorrect greedy heuristic appeared most convincing before you tested it?**

[Team to answer in their own words.] A draft answer: Earliest Start looked the most convincing. "Start working as soon as possible" sounds like a sensible way to use time, and it is correct on most random instances (71% optimal in Part 5). Its failure needs one long early job that blocks the rest, which is easy to overlook. Shortest Duration also looked plausible, since short jobs seem to leave room for others. The Sanity Tests showed that both intuitions break on small, specific inputs.

**2. What did the counterexample reveal about why the local rule fails?**

Each failing rule makes its choice based on one number and ignores how that choice affects the rest of the timeline. EST ignores how long a job runs. SD ignores where a job sits relative to other jobs, so a short job that spans a boundary can block two compatible jobs. LD prefers jobs that cover the most time, which means it selects jobs that overlap the most others. EFT succeeds because finish time captures what matters for the future: the earlier a job ends, the more of the timeline remains free. The exchange argument depends on this property, and none of the three failing rules has it.

**3. What did the exact solver contribute to the development process?**

The exact solver gave us a ground truth to test against. Without it we could only tell that a heuristic produced a schedule, not whether the schedule was the best possible. It let us check the Sanity Tests and every counterexample objectively, and it supplied the optimum `OPT(I)` used in every ratio in Parts 4 and 5. Because the solver is simple enough to trust, any disagreement could be attributed to the greedy implementation rather than the oracle. It is slow, so we only used it on small instances, but that was enough to validate the method.

**4. What is the difference between experimentally validating an algorithm and proving it correct?**

Experiments can only show that an implementation agrees with the reference on the cases that were tested. Our Part 4 result (100 of 100 matches) is strong evidence that our EFT implementation is working, but the test cases are random and small (`n = 15`). An error that only appears for other distributions, larger `n`, or unusual tie patterns would not show up. A proof covers every input at once. The exchange argument for EFT is such a proof: it shows that replacing the first job of any optimal schedule with EFT's first job never loses a job, and induction over the remaining jobs extends this to the whole schedule. The experiments support the proof and catch implementation bugs, but they do not replace it.

### Conclusions

Earliest Finish Time matched the exact optimum on all 100 Part 4 instances and on all 120 Part 5 instances. The three alternative rules each fail, and the failures have a clear pattern: each one ignores either how long a job runs, where it sits relative to other jobs, or how much of the timeline it blocks. Runtime is dominated by the `O(n log n)` sort, and the measured timings are consistent with that. The main limitation is the sample size and instance size: we tested small random instances, so the results are evidence rather than proof. The proof of EFT's optimality is the exchange argument described above.

---

## AI Use Statement

[Team to complete: list the tools used and how they contributed, or state that no generative AI tools were used.]

## Group Contribution Statement

[Team to complete: primary contribution of each member.]
