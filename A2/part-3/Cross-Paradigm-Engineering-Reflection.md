## Part III. Cross-Paradigm Engineering Reflection

### 1. What work does divide and conquer avoid in inversion counting?

Divide and conquer splits the array and uses sorted halves to count cross inversions during the merge step, which allows it to avoid checking every pair of array elements. 

### 2. Why are inversion-counting subproblems independent, but coin-change subproblems overlap?

Inversion counting subproblems are independent because each recursive call processes a separate half of the array, and the results are then combined during the merge. Whereas in coin change, multiple sequences of choices could leave the same remaining amount. If you take coins {1, 3, 4} and target 6, taking 4 leaves 2, and taking 1 and then 3 also leaves 2.

### 3. What role does sorting play in inversion counting?

Inversions are easy to count if you sort each half. For example, we know that if the next element in the right half is smaller than the next element in the left half, it's also smaller than all remaining elements in the sorted left half. So, instead of checking every pair separately, we can count all inversions at once. 

### 4. Why can naive recursion and memoization have very different runtimes?

Naive recursion and memoization can have very different runtimes because even though both use the same recurrence, the naive solver has to recompute amounts whenever a different path reaches them. The memoized solver stores each answer and reuses it, which can massively reduce the amount of calls. In Part 2C at A = 25, naive recursion made 229,970 calls, while memoization made only 71 calls.
### 5. How did baseline and exact solvers help validate optimized algorithms?

For coin change, we compared the naive, memoized and bottom-up solvers to check that they all returned the same optimal number of coins. Baseline and exact solvers help validate optimized algoriths because we can directly compare the brute-force inversion counter result with the divide-and-conquer counter result. 

Our group's greedy-counterexample CSV also gives cases that show why greedy cannot replace an exact coin-change solver:

| Denominations | Target | Greedy | Optimal |
|---|---:|---|---|
| {1, 3, 4} | 6 | 4 + 1 + 1 (3 coins) | 3 + 3 (2 coins) |
| {1, 4, 5} | 8 | 5 + 1 + 1 + 1 (4 coins) | 4 + 4 (2 coins) |
| {1, 4, 6} | 8 | 6 + 1 + 1 (3 coins) | 4 + 4 (2 coins) |

For the first case, greedy chooses 4 because it is the largest available coin. That leaves two 1s, while choosing two 3s gives a better overall solution.

### 6. When would you try divide and conquer versus dynamic programming?

Divide and conquer could be used if a problem can be split into small and independent sub-problems. An example is inversion counting, as the left and right halves can be solved separately. Dynamic programming would be used if there were many recursive paths that all lead to the same subproblems and a best answer could be built from smaller optimal answers. An example is coin change, because the same remaining amount occurs repeatedly.

