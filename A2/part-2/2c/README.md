# CMP_SC 4050 GEA2 — Part 2C

## Run

Keep `part2c_experiments.py` beside the completed `algorithms.py`, then run:

```
python part2c_experiments.py
```

It first runs 239 small validations using the group's actual three exact solvers. The script then writes `part2c_experiment1.csv` and `part2c_experiment2.csv`. Experiments use `COINS = [1,3,4]` and fixed seed 42 for the extra randomized tests.

Experiment 1 tries targets 5,10,... until naive recursion reaches the 250,000-call safety cutoff. Counted recursive functions repeat the actual nested recurrence from the group's naive and memoized functions; assertions confirm completed answers match the original functions. The memoized instrumentation starts with `{0:0}`, so calls to base case 0 count as cache hits.

Experiment 2 times the group's **actual** `coin_change_dp` implementation on targets `2**8` through `2**18`, with seven timing repetitions per target. Times include the function's coin-list reconstruction, but not CSV export. CSVs in this package reflect the local measurement run; rerunning them will change timing values.


