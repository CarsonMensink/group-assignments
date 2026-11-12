# algorithms.py
from typing import List, Optional, Tuple

def coin_change_greedy(coins: List[int], amount: int) -> Tuple[int, Optional[List[int]]]:
    """
    Part 2A.A: Greedy Largest-Denomination First
    Repeatedly takes the largest coin <= remaining amount.
    Returns (coin_count, coin_list) or (-1, None) if it gets stuck.
    """
    # TODO: 
    pass


def coin_change_naive(coins: List[int], amount: int) -> int:
    """
    Part 2A.B: Naive Exact Recursive Solver
    Pure exponential recursion trying every possible final coin (-1 if impossible).
    """
    # TODO: 
    pass


def coin_change_memo(coins: List[int], amount: int) -> int:
    """
    Part 2A.C: Top-Down DP with Memoization
    Recursive solver with a cache for subproblems (-1 if impossible).
    """
    # TODO: 
    pass


def coin_change_dp(coins: List[int], amount: int) -> Tuple[int, Optional[List[int]]]:
    """
    Part 2A.D: Bottom-Up DP
    Iterative DP building up the table from 0 to amount.
    Returns (min_coins, coin_list) or (-1, None).
    """
    # TODO: 
    pass