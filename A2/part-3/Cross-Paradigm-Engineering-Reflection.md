## Part III. Cross-Paradigm Engineering Reflection

### 1. What work does divide and conquer avoid in inversion counting?

The brute-force counter checks all n(n − 1)/2 pairs. Divide and conquer instead counts inversions inside each half recursively and counts cross inversions while merging the sorted halves. If the next right element is smaller than the next left element, it is smaller than every remaining left element. The merge adds the number of remaining left elements at once, avoiding separate comparisons for those pairs. Each merge level takes O(n) work and there are O(log n) levels, reducing total time from Θ(n²) to Θ(n log n).

### 2. Why are inversion-counting subproblems independent, but coin-change subproblems overlap?

Inversion counting's recursive calls operate on disjoint index ranges. Each call counts inversions within its own half, and the merge separately handles pairs crossing the split. Neither half needs the other half's recursive answer to solve its own internal problem. Equal values in different halves do not make them the same subproblem, because their index ranges differ.

Coin-change subproblems are identified by the remaining amount for a fixed denomination system. Different choice sequences can reach the same amount: with {1, 3, 4} and target 6, taking 4 leaves 2, and taking 1 followed by 3 also leaves 2. Both paths need the same OPT(2). Naive recursion solves it again, while memoization can reuse the cached result.

### 3. What role does sorting play in inversion counting?

Sorting each half provides the order needed to count cross inversions in batches. If right[j] < left[i], then right[j] is smaller than all len(left) − i remaining left elements, so the merge adds that many inversions. If left[i] ≤ right[j], it takes the left element without adding inversions; taking the left on equality prevents equal values from being counted.

We cannot simply sort the whole original array first, because that would erase the order whose inversions we need to measure. The algorithm counts internal inversions before returning sorted halves. Sorting within a half preserves the cross-inversion count because every original left-half position precedes every original right-half position. The sorted output is therefore both a result of the recursion and the information needed for the next merge.

### 4. Why can naive recursion and memoization have very different runtimes?

Both evaluate the same optimal-substructure recurrence, but naive recursion expands a new recursive subtree whenever an amount is reached again. Memoization computes each reached amount once and returns cached answers on later requests. There are at most A + 1 distinct nonnegative amounts, and each computed state examines at most k denominations, giving O(kA) recurrence time instead of the naive method's potentially exponential time.

Part 2C makes the difference visible: at A = 25 with {1, 3, 4}, naive recursion made 229,970 calls to only 26 distinct amounts. Memoization made 71 calls, including 46 cache hits. Its 25 positive states were computed once each, with state 0 cached initially. At A = 30, naive recursion reached the 250,000-call cutoff while memoization completed in 86 calls. The tradeoff is retaining cached answers and predecessor choices, using O(A) space for fixed denominations. Memoization also retains recursive stack depth and pseudo-polynomial dependence on A.

### 5. How did baseline and exact solvers help validate optimized algorithms?

For inversion counting, the brute-force algorithm follows the pair definition directly, so it serves as an oracle for the faster divide-and-conquer method. Part 1B reports agreement on all 365 cases, including 15 hand-checkable arrays, 300 random distinct arrays, and 50 arrays with duplicates. The checks also verify sorted output and that the input is unchanged. The duplicate cases are especially useful for catching an incorrect tie rule.

For coin change, Part 2B compares the optimal counts from naive recursion, memoization, and bottom-up DP on 12 hand-checkable cases and 150 randomized cases. Its independent validator checks that returned coins are allowed, sum to the target, and match the reported count. Hand-counted impossible cases help check failure results. Part 2C adds 239 small cross-checks before its experiments. Agreement provides evidence on tested inputs; the correctness arguments are still needed because shared bugs could make several implementations agree on a wrong answer.

Our group's greedy-counterexample CSV also gives cases that show why greedy cannot replace an exact coin-change solver:

| Denominations | Target | Greedy | Optimal |
|---|---:|---|---|
| {1, 3, 4} | 6 | 4 + 1 + 1 (3 coins) | 3 + 3 (2 coins) |
| {1, 4, 5} | 8 | 5 + 1 + 1 + 1 (4 coins) | 4 + 4 (2 coins) |
| {1, 4, 6} | 8 | 6 + 1 + 1 (3 coins) | 4 + 4 (2 coins) |

For the first case, greedy chooses 4 because it is the largest available coin. That leaves two 1s, while choosing two 3s gives a better overall solution. After cross-validating the exact methods, Part 2B uses bottom-up DP as the oracle for 2,275 small search instances and finds 197 suboptimal greedy results. The three examples above are exported from distinct denomination systems.

### 6. When would you try divide and conquer versus dynamic programming?

I would try divide and conquer when a problem splits into smaller independent instances and their answers can be combined efficiently. Inversion counting fits because the left and right index ranges are disjoint and a linear merge handles the cross pairs. Caching those recursive calls would add little benefit because the same index-range problem is not repeatedly solved.

I would try dynamic programming when different recursive paths reach the same states and a state has an optimal answer that can be built from smaller states. Coin change fits because the remaining amount captures the subproblem and removing a coin reduces it to a smaller amount. Top-down memoization can avoid states that are never reached, while bottom-up evaluation avoids Python's recursion-depth limit. Before choosing either, I would estimate the number of states and transitions: an O(kA) DP can still be impractical for a very large binary-encoded target, even though it removes repeated computation.
