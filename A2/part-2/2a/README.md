# Part 2A: Four Coin-Change Solvers

`algorithms.py` implements four solvers for the minimum-coin change problem:

| Function | Method | Exact? |
|---|---|---|
| `coin_change_greedy` | Largest-denomination-first heuristic | No |
| `coin_change_naive` | Optimal-substructure recurrence, no memoization | Yes |
| `coin_change_memo` | Same recurrence, top-down with a cache | Yes |
| `coin_change_dp` | Bottom-up table over amounts 0, 1, …, A | Yes |

Language: Python 3.10+ (developed with 3.14). Standard library only.

## Common interface

```python
def solver(coins: List[int], amount: int) -> Tuple[int, Optional[List[int]]]
```

| Situation | Return value |
|---|---|
| Feasible | `(coin_count, chosen_coins)` where `len(chosen_coins) == coin_count` and `sum(chosen_coins) == amount` |
| `amount == 0` | `(0, [])` |
| Impossible (IMPOSSIBLE) | `(-1, None)` |
| `amount < 0` or a coin `<= 0` | raises `ValueError` |

- The caller's `coins` list is never mutated. Each solver works on a sorted, de-duplicated copy.
- Behaviour is deterministic. The three exact solvers break ties toward the smaller coin, so they return **identical** lists.
- For greedy only, `(-1, None)` means *greedy got stuck*. It does **not** mean that no solution exists: for `coins=[3, 5]`, `amount=9`, greedy gets stuck even though `3+3+3` works.

```python
>>> from algorithms import *
>>> coin_change_greedy([1, 3, 4], 6)
(3, [4, 1, 1])
>>> coin_change_dp([1, 3, 4], 6)
(2, [3, 3])
>>> coin_change_memo([2], 3)
(-1, None)
```

---

## Time and auxiliary-space analysis

**Cost model.** We assume a word-RAM, so integer arithmetic, comparisons and list indexing cost Θ(1). Python `set`/`dict` operations cost Θ(1) expected, so bounds that use them are expected bounds. Auxiliary space excludes the input. The returned list costs Θ(m) in every solver and is not counted as auxiliary space.

| Symbol | Meaning |
|---|---|
| n | `len(coins)`, which may include duplicates |
| k | number of distinct denominations (k ≤ n) |
| c, d_max | smallest and largest coin |
| L | ⌊A / c⌋, the most coins any solution can use, and the deepest recursion |
| m | number of coins returned (m ≤ L ≤ A) |
| j(r) | number of coins ≤ r, i.e. the inner-loop iterations at amount r (j(r) ≤ k) |
| S | distinct amounts visited by the recursive solvers; L + 1 ≤ ∣S∣ ≤ A + 1 |

**Shared preprocessing (`_prepare`).** Validation and de-duplication take Θ(n) time, and sorting the k distinct coins takes Θ(k log k) time in the worst case (Ω(k) if they are already in order). This step uses Θ(k) auxiliary space. We write P = Θ(n + k log k) for this cost. Every solver below pays P once.

### Greedy

- **Time.** The main loop runs at most k iterations, each costing Θ(1), plus Θ(copies taken) for `extend`. The copies total m over the whole loop. So T_greedy = Θ(n + k log k + m) in the worst case and Ω(n + m) on every input. The bound is tight because D = {1} forces m = A.
- **Auxiliary space.** The sorted copy of the coins takes Θ(k). Each `[coin] * take` also creates a temporary list of length `take`, even though the returned list is excluded from auxiliary space. For successful runs, this gives O(k + m) auxiliary space, tight at Θ(k + m) in the worst case: D = {1} creates a temporary list of length m = A.

### Naive recursion

Let N(a) be the number of `solve` calls that `solve(a)` makes. The code gives the recurrence exactly:

```
N(0) = 1
N(a) = 1 + Σ_{d ∈ D, d ≤ a} N(a − d)
```

- **Time.** Each call does Θ(1) work plus one loop iteration per child call, plus at most one `break`. So the recursion costs Θ(N(A)), and reconstruction adds only Θ(m). This gives T_naive = Θ(P + N(A)).
  - **k = 1:** the calls form one chain, so N(A) = L + 1 = Θ(A / c).
  - **k ≥ 2:** let ρ > 1 be the unique root of Σ_{d ∈ D} ρ^(−d) = 1. Induction on the recurrence gives ρ^(A − d_max) ≤ N(A) ≤ α·ρ^A, where α is a constant that depends only on D. So N(A) = Θ(ρ^A), which is exponential in A.
  - **Bounds in terms of k alone:** k^(A/d_max − 1) ≤ N(A) ≤ (k^(L+1) − 1) / (k − 1). The upper bound holds because the call tree has depth at most L and branching factor at most k.
  - **Example:** for D = {1, 2}, N(A) = F(A+3) − 1 = Θ(1.618^A), where F(i) is the i-th Fibonacci number.
- **Auxiliary space.** The first descent A → A − c → … is the deepest chain, so the stack holds exactly L + 1 frames, Θ(L). The write-only `choice` table holds at most |S| entries. In total, Θ(k + A) in the worst case, Ω(k + L) on every input, and Θ(k + A) whenever 1 ∈ D.

### Top-down memoization

- **Time.** Each amount r ∈ S is computed once, at a cost of Θ(1 + j(r)). Every other call is a Θ(1) cache hit, and each such call corresponds to a loop iteration that has already been counted. So T_memo = Θ(P + Σ_{r ∈ S} (1 + j(r))).
  - **Upper bound:** O(P + kA), because |S| ≤ A + 1 and j(r) ≤ k.
  - **Lower bound:** Ω(P + L) on every input, because S always contains the chain A, A − c, ….
  - **Worst case:** Θ(n + k log k + kA), including validation of all n input coins even when some are duplicates. The kA term is attained by D = {1, …, k} with A ≥ 2k.
- **Auxiliary space.** `memo` holds |S| entries and `choice` holds at most |S|. The stack depth is exactly L + 1 ≤ |S|. In total, Θ(k + |S|), which is Θ(k + A) in the worst case and Ω(k + L) on every input. Memo visits only the amounts reachable from A. For example, with D = {10, 20} and A = 1000 it solves 101 states, while bottom-up DP fills all 1001.

### Bottom-up DP

- **Time.** The outer loop runs A times, and the inner loop costs Θ(1 + j(a)) at amount a. Since Σ_{a=1..A} j(a) = Σ_{d ≤ A} (A − d + 1), the following holds exactly on every input: T_dp = Θ(P + A + Σ_{d ≤ A} (A − d + 1)). It is O(P + kA) and Ω(P + A) on every input, and Θ(P + kA) whenever d_max ≤ A/2.
- **Auxiliary space.** The two tables take Θ(A), so Θ(k + A) on every input. There is no recursion.

### Summary

| Solver | Worst-case time | Lower bound (every input) | Auxiliary space |
|---|---|---|---|
| Greedy | Θ(n + k log k + m) | Ω(n + m) | Θ(k + m) worst case for successful runs |
| Naive | Θ(P + N(A)); N(A) = Θ(ρ^A) if k ≥ 2, L + 1 if k = 1 | Ω(k^(A/d_max − 1)) for k ≥ 2, A ≥ d_max | Θ(k + A) worst, Ω(k + L) |
| Memo | Θ(n + k log k + kA) | Ω(P + L) | Θ(k + A) worst, Ω(k + L) |
| Bottom-up | Θ(n + k log k + kA) | Ω(P + A) | Θ(k + A) always |

**Notes.**
- Θ(kA) is *pseudo-polynomial*. Writing A down takes only about log₂ A bits, so the work grows exponentially in the input length.
- Both recursive solvers reach a stack depth of L + 1. For large targets, they may hit Python's recursion limit; use `coin_change_dp` instead.
