## Part 2C. Memoization and Pseudo-Polynomial Behavior

### Experiment 1: Repeated Subproblems

I used our group's Part 2A solvers with denominations {1, 3, 4} and tested targets 5, 10, 15, 20, 25, and 30. Both the naive and memoized solvers use the same recurrence, where OPT(0) = 0 and OPT(A) = 1 + min(OPT(A − d)) for each coin d that fits. The difference is that naive recursion recalculates amounts whenever they are reached, while memoization stores the answers.

I counted recursive calls, distinct amounts reached, and cache hits. The memoized solver starts with 0 already cached, so it is included in the state count and counted as a cache hit when used. I also set a cutoff of 250,000 calls for naive recursion to prevent it from running too long. For the stopped run, the state count includes amounts reached but not necessarily finished.

| Target A | Naive calls | Naive distinct states | Memoized calls | Memoized states | Cache hits |
|---:|---:|---:|---:|---:|---:|
| 5 | 15 | 6 | 11 | 6 | 6 |
| 10 | 168 | 11 | 26 | 11 | 16 |
| 15 | 1,869 | 16 | 41 | 16 | 26 |
| 20 | 20,736 | 21 | 56 | 21 | 36 |
| 25 | 229,970 | 26 | 71 | 26 | 46 |
| 30 | 250,000 (stopped) | 31 | 86 | 31 | 56 |

At A = 25, naive recursion made 229,970 calls despite there only being 26 different amounts. Memoization only made 71 calls, with 46 of those being cache hits. At A = 30, naive recursion reached the safety cutoff. This shows how much repeated work memoization avoids, even though both algorithms use the same recurrence. Naive recursion can take exponential time, while memoization takes O(kA) time and O(A) space in the worst case, where k is the number of denominations.

### Experiment 2: Pseudo-Polynomial Scaling

I kept the denominations {1, 3, 4} the same and increased A from 2⁸ to 2¹⁸, doubling it each time. For each target, I ran the group's bottom-up solver seven times and recorded the median runtime. The timing includes preprocessing and reconstructing the coin list, but not printing or writing the results to a file. I also counted the DP states from 0 through A, giving A + 1 states total. The tests were run using Python 3.13.5 on Linux, so runtimes could be different on another machine.

| Target A | Bits in A | DP states | Median runtime (ms) |
|---:|---:|---:|---:|
| 256 | 9 | 257 | 0.0634 |
| 512 | 10 | 513 | 0.1367 |
| 1,024 | 11 | 1,025 | 0.2878 |
| 2,048 | 12 | 2,049 | 0.6216 |
| 4,096 | 13 | 4,097 | 1.2880 |
| 8,192 | 14 | 8,193 | 2.6022 |
| 16,384 | 15 | 16,385 | 5.3843 |
| 32,768 | 16 | 32,769 | 11.1307 |
| 65,536 | 17 | 65,537 | 23.1644 |
| 131,072 | 18 | 131,073 | 45.4883 |
| 262,144 | 19 | 262,145 | 94.2407 |

Bottom-up DP processes A + 1 states and checks up to k coins for each amount, giving it a runtime of O(kA). Our results show that when A doubles, the runtime also roughly doubles. However, the number of bits needed to represent A only increases by one each time it doubles. Since A grows exponentially with the number of bits used to represent it, O(kA) can also be exponential in the input length. This is why bottom-up DP is considered pseudo-polynomial, as its runtime depends on the actual value of A rather than just the number of bits needed to represent it.

### Validation

Before running the experiments, I compared the group's naive, memoized, and bottom-up solvers on 239 cases. This included 39 small cases with targets 0–12 using denominations {1, 3, 4}, {1, 4, 6}, and {4, 6}, along with 200 randomly generated cases using seed 42.

All three solvers returned the same optimal counts and coin lists. I also checked that the bottom-up solutions used valid coins, had the correct number of coins, and added up to the target amount. These tests helped validate the Part 2C experiments, but they don't replace the group's full Part 2B validation.
