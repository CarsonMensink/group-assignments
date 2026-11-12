# algorithms.py
from typing import Dict, List, Optional, Tuple

INF = float("inf")

Result = Tuple[int, Optional[List[int]]]


def _prepare(coins: List[int], amount: int) -> List[int]:
    """Validate inputs and return a sorted, de-duplicated copy of the coins (input is not mutated)."""
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if any(c <= 0 for c in coins):
        raise ValueError("all coin denominations must be positive integers")
    return sorted(set(coins))


def coin_change_greedy(coins: List[int], amount: int) -> Result:
    """
    Part 2A.A: Greedy Largest-Denomination First
    Repeatedly takes the largest coin <= remaining amount.
    Returns (coin_count, coin_list) or (-1, None) if it gets stuck.
    """
    denoms = _prepare(coins, amount)
    remaining = amount
    chosen: List[int] = []

    # Walk denominations from largest to smallest, taking as many of each as fit.
    for coin in reversed(denoms):
        if remaining == 0:
            break
        take = remaining // coin
        if take:
            chosen.extend([coin] * take)
            remaining -= take * coin

    # Greedy got stuck: no remaining coin fits the leftover amount.
    if remaining != 0:
        return -1, None
    return len(chosen), chosen


def coin_change_naive(coins: List[int], amount: int) -> Result:
    """
    Part 2A.B: Naive Exact Recursive Solver
    Pure exponential recursion trying every possible final coin (-1 if impossible).
    Returns (min_coins, coin_list) or (-1, None).
    """
    denoms = _prepare(coins, amount)
    # Write-only during the recursion: records the optimal coin for each solved
    # amount so a solution can be rebuilt afterwards. It is never read to skip
    # work, so every subproblem is still recomputed each time (no memoization).
    choice: Dict[int, int] = {}

    # Pure recurrence: M(0) = 0, M(r) = 1 + min over coins d <= r of M(r - d).
    def solve(remaining: int) -> float:
        if remaining == 0:
            return 0
        best = INF
        for coin in denoms:  # ascending order -> deterministic tie-breaking
            if coin > remaining:
                break
            sub = solve(remaining - coin)
            if sub + 1 < best:
                best = sub + 1
                choice[remaining] = coin
        return best

    count = solve(amount)
    if count == INF:
        return -1, None

    # Reconstruct by following the recorded coin choices back down to 0.
    chosen: List[int] = []
    remaining = amount
    while remaining > 0:
        coin = choice[remaining]
        chosen.append(coin)
        remaining -= coin
    return int(count), chosen


def coin_change_memo(coins: List[int], amount: int) -> Result:
    """
    Part 2A.C: Top-Down DP with Memoization
    Recursive solver with a cache for subproblems (-1 if impossible).
    Returns (min_coins, coin_list) or (-1, None).
    Note: recursion depth can reach amount // min(coins); very large amounts
    may exceed Python's default recursion limit.
    """
    denoms = _prepare(coins, amount)
    memo: Dict[int, float] = {0: 0}
    choice: Dict[int, int] = {}  # remaining amount -> coin used first in an optimal solution

    # Solve each remaining amount once; later requests reuse the cached answer.
    def solve(remaining: int) -> float:
        if remaining in memo:
            return memo[remaining]
        best = INF
        for coin in denoms:  # ascending order -> deterministic tie-breaking
            if coin > remaining:
                break
            sub = solve(remaining - coin)
            if sub + 1 < best:
                best = sub + 1
                choice[remaining] = coin
        memo[remaining] = best
        return best

    count = solve(amount)
    if count == INF:
        return -1, None

    # Reconstruct by following the stored coin choices back down to 0.
    chosen: List[int] = []
    remaining = amount
    while remaining > 0:
        coin = choice[remaining]
        chosen.append(coin)
        remaining -= coin
    return int(count), chosen


def coin_change_dp(coins: List[int], amount: int) -> Result:
    """
    Part 2A.D: Bottom-Up DP
    Iterative DP building up the table from 0 to amount.
    Returns (min_coins, coin_list) or (-1, None).
    """
    denoms = _prepare(coins, amount)
    best = [INF] * (amount + 1)
    last_coin = [0] * (amount + 1)  # predecessor coin for reconstruction
    best[0] = 0

    # Fill the table in increasing order so every smaller state is already optimal.
    for a in range(1, amount + 1):
        for coin in denoms:  # ascending order -> deterministic tie-breaking
            if coin > a:
                break
            if best[a - coin] + 1 < best[a]:
                best[a] = best[a - coin] + 1
                last_coin[a] = coin

    if best[amount] == INF:
        return -1, None

    # Walk predecessor coins from amount back to 0 to recover the multiset.
    chosen: List[int] = []
    a = amount
    while a > 0:
        chosen.append(last_coin[a])
        a -= last_coin[a]
    return int(best[amount]), chosen
