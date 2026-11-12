# main.py
import random
import csv
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Allow this script to import the Part 2A algorithms module from the sibling folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2a"))

from algorithms import (
    coin_change_greedy,
    coin_change_naive,
    coin_change_memo,
    coin_change_dp,
)

# ==============================================================================
# INDEPENDENT SOLUTION VALIDATOR
# ==============================================================================

def validate_solution(coins: List[int], amount: int, count: int, coin_list: Optional[List[int]]) -> None:
    if count == -1:
        assert coin_list is None, f"Expected None list for impossible case (D={coins}, A={amount})"
        return

    assert coin_list is not None, f"Missing coin list for feasible case (D={coins}, A={amount})"
    assert len(coin_list) == count, f"Count mismatch: reported {count}, list has {len(coin_list)}"
    assert sum(coin_list) == amount, f"Sum mismatch: sum({coin_list}) != {amount}"
    
    coin_set = set(coins)
    for c in coin_list:
        assert c in coin_set, f"Invalid coin {c} used; not in {coins}"


# ==============================================================================
# VALIDATION SUITE & TEST RUNNER
# ==============================================================================

def run_validation_suite() -> None:
    hand_tests = [
        ([1, 5, 10, 25], 0, 0, "Amount requested is 0"),
        ([2, 4, 6], 7, -1, "Impossible odd target from even coins"),
        ([5, 10], 3, -1, "Impossible target smaller than smallest coin"),
        ([1, 3, 4], 6, 2, "Multiple optimal / classic greedy trap (3+3)"),
        ([1, 2, 5], 11, 3, "Similar to US currency"),
        ([1, 5, 6, 9], 11, 2, "6+5 vs greedy 9+1+1"),
    ]

    print("--- Running Hand-Checkable Test Cases ---")
    for coins, amount, expected, desc in hand_tests:
        c_dp, list_dp = coin_change_dp(coins, amount)
        assert c_dp == expected, f"DP disagreement on '{desc}': got {c_dp}, expected {expected}"
        validate_solution(coins, amount, c_dp, list_dp)
    print("Hand-checkable tests passed successfully!\n")


# ==============================================================================
# AUTOMATED GREEDY COUNTEREXAMPLE SEARCH & CSV EXPORT
# ==============================================================================

def search_greedy_counterexamples(max_coin: int = 15, max_amount: int = 6) -> List[dict]:
    counterexamples = []
    for c2 in range(2, max_coin):
        for c3 in range(c2 + 1, max_coin + 1):
            coins = [1, c2, c3]
            for amount in range(1, max_amount + 1):
                dp_count, dp_list = coin_change_dp(coins, amount)
                gr_count, gr_list = coin_change_greedy(coins, amount)

                if dp_count != -1 and gr_count != -1 and gr_count > dp_count:
                    counterexamples.append({
                        "D": coins,
                        "A": amount,
                        "greedy_count": gr_count,
                        "greedy_coins": gr_list,
                        "opt_count": dp_count,
                        "opt_coins": dp_list,
                        "gap": gr_count - dp_count,
                    })
    return counterexamples


if __name__ == "__main__":
    print("Starting pipeline...")
    run_validation_suite()