## Part 2C. Memoization and Pseudo-Polynomial Behavior

### Experiment 1: Repeated Subproblems

I used denominations {1, 3, 4} and tested targets 5, 10, 15, 20, 25, and 30. Both the group's naive and memoized solvers use the same recurrence, where OPT(0) = 0 and OPT(A) = min{1 + OPT(A − d) : d ≤ A}. A positive amount with no feasible candidate has value infinity. The difference is that naive recursion recalculates amounts whenever they are reached, while memoization stores the answers. For call counting, the experiment uses instrumented copies of the recursive recurrence with the same ascending coin order. Completed answers are checked against the actual Part 2A solvers; these counts do not include preprocessing or solution reconstruction.

I counted recursive calls, distinct amounts reached, and cache hits. The memoized solver starts with 0 already cached, so it is included in the state count and counted as a cache hit when used. I also set a cutoff of 250,000 calls for naive recursion to prevent it from running too long. For the stopped run, the state count includes amounts reached but not necessarily finished.

| Target A | Naive calls | Naive distinct states | Memoized calls | Memoized states | Cache hits |
|---:|---:|---:|---:|---:|---:|
| 5 | 15 | 6 | 11 | 6 | 6 |
| 10 | 168 | 11 | 26 | 11 | 16 |
| 15 | 1,869 | 16 | 41 | 16 | 26 |
| 20 | 20,736 | 21 | 56 | 21 | 36 |
| 25 | 229,970 | 26 | 71 | 26 | 46 |
| 30 | 250,000 (stopped) | 31 | 86 | 31 | 56 |

At A = 25, naive recursion made 229,970 calls despite there only being 26 different amounts. Memoization only made 71 calls, with 46 of those being cache hits. Its 25 uncached positive states were each computed once, and state 0 was already cached. At A = 30, naive recursion reached the safety cutoff; 250,000 is a lower bound on the calls needed to finish, not a completed measurement. Memoization completed with 86 calls. This shows how much repeated work memoization avoids, even though both algorithms use the same recurrence. Naive recursion can take exponential time, while memoization takes O(kA) time and O(A) space for the recurrence, where k is the number of denominations. The cache, predecessor choices, and recursion stack all fit within that space bound for fixed denominations.

### Experiment 2: Pseudo-Polynomial Scaling

I kept the denominations {1, 3, 4} the same and increased A from 2⁸ to 2¹⁸, doubling it each time. For each target, I ran the group's actual bottom-up solver seven times using `time.perf_counter()` and recorded the median runtime. The timing includes preprocessing and reconstructing the coin list, but not validation, printing, or writing results to a file. The table has A + 1 states, including base state 0; A positive states are processed by the main loop. The results below match `part2c_experiment2.csv`, generated with Python 3.14.3 on an Apple M3 (macOS, arm64). Timings can change with hardware, system load, and Python version.

| Target A | Bits in A | DP states | Median runtime (ms) |
|---:|---:|---:|---:|
| 256 | 9 | 257 | 0.0887 |
| 512 | 10 | 513 | 0.1896 |
| 1,024 | 11 | 1,025 | 0.3925 |
| 2,048 | 12 | 2,049 | 0.8245 |
| 4,096 | 13 | 4,097 | 1.7005 |
| 8,192 | 14 | 8,193 | 3.4363 |
| 16,384 | 15 | 16,385 | 7.0112 |
| 32,768 | 16 | 32,769 | 13.8394 |
| 65,536 | 17 | 65,537 | 27.8256 |
| 131,072 | 18 | 131,073 | 55.0530 |
| 262,144 | 19 | 262,145 | 110.6298 |

Bottom-up DP allocates A + 1 states and checks up to k coins for each positive amount, giving O(kA) time and O(A) table space for fixed denominations. Our results show roughly linear growth in A, with measurement noise: the final three doublings multiply runtime by approximately 2.01, 1.98, and 2.01. These measurements support the complexity analysis; they do not establish it by themselves.

The number of bits needed to represent A only increases by one each time A doubles. If b = floor(log₂ A) + 1, then A can be as large as 2ᵇ − 1. For the tested powers of two, A = 2^(b − 1), so the table size and work grow exponentially in b even though they grow linearly in A. This is why O(kA) is pseudo-polynomial: its bound depends on the numeric target, rather than being polynomial in the binary input length. Memoization avoids repeated states, but it does not remove this dependence when all amounts from 0 to A are reached, as happens here because denomination 1 is present.

### Validation

Before running the experiments, I compared the group's naive, memoized, and bottom-up solvers on 239 cases. This included 39 small cases with targets 0–12 using denominations {1, 3, 4}, {1, 4, 6}, and {4, 6}, along with 200 randomly generated cases using seed 42.

All three solvers returned the same optimal counts and coin lists. I also checked that the bottom-up solutions used valid coins, had the correct number of coins, and added up to the target amount. These tests helped validate the Part 2C experiments, but they don't replace the group's full Part 2B validation.

### Reproducing the experiments

From the repository root, run `python3 A2/part-2/2c/part2c_experiments.py` with Python 3.10 or newer and no third-party packages. Use normal Python execution, since `python -O` disables the validation assertions. The script runs validation, writes both experiment CSVs beside itself, and prints the results. The call counts are deterministic; runtime values will vary on rerun.
