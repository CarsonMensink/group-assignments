import random
from typing import List, Optional, Tuple
import csv

# ==============================================================================
# 1. EXACT & GREEDY SOLVERS
# ==============================================================================


def coin_change_naive(coins: List[int], amount: int) -> int:
    #Pure exponential recursion returning minimum coin count (-1 if impossible).
    if amount == 0:
        return 0
    if amount < 0:
        return -1

    min_coins = float("inf")
    for c in coins:
        res = coin_change_naive(coins, amount - c)
        if res != -1:
            min_coins = min(min_coins, res + 1)

    return -1 if min_coins == float("inf") else int(min_coins)


def coin_change_memo(coins: List[int], amount: int) -> int:
    #Top-down memoized DP returning minimum coin count (-1 if impossible).
    memo = {}

    def helper(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return -1
        if rem in memo:
            return memo[rem]

        min_coins = float("inf")
        for c in coins:
            res = helper(rem - c)
            if res != -1:
                min_coins = min(min_coins, res + 1)

        memo[rem] = -1 if min_coins == float("inf") else int(min_coins)
        return memo[rem]

    return helper(amount)


def coin_change_dp( coins: List[int], amount: int) -> Tuple[int, Optional[List[int]]]:
    #Bottom-up DP returning (min_coins, coin_list).
    #Returns (-1, None) if amount cannot be formed.
    
    dp = [float("inf")] * (amount + 1)
    parent = [-1] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0 and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                parent[a] = c

    if dp[amount] == float("inf"):
        return -1, None

    # Reconstruct optimal coin list
    res_coins = []
    curr = amount
    while curr > 0:
        c = parent[curr]
        res_coins.append(c)
        curr -= c

    return int(dp[amount]), res_coins


def coin_change_greedy( coins: List[int], amount: int) -> Tuple[int, Optional[List[int]]]:
    #Repeatedly takes the largest coin that is <= remaining amount.
    #Returns (coin_count, coin_list) or (-1, None) if greedy gets stuck.
    
    sorted_coins = sorted(coins, reverse=True)
    rem = amount
    used = []

    for c in sorted_coins:
        while rem >= c:
            rem -= c
            used.append(c)

    if rem != 0:
        return -1, None
    return len(used), used


def inspect_dp_table(coins: List[int], amount: int) -> None:
    #Prints the step-by-step DP table filling and parent pointer selection. 
    dp = [float("inf")] * (amount + 1)
    parent = [-1] * (amount + 1)
    dp[0] = 0

    print(f"\n--- DP Table Trace for D={coins}, A={amount} ---")
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0 and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                parent[a] = c
        status = f"min_coins={dp[a] if dp[a] != float('inf') else 'INF'}, parent_coin={parent[a]}"
        print(f"Amount {a:2d} -> {status}")
    print("-" * 45)


# ==============================================================================
# 2. INDEPENDENT SOLUTION VALIDATOR
# ==============================================================================


def validate_solution(coins: List[int], amount: int, count: int, coin_list: Optional[List[int]]) -> None:
    #Independently verifies feasibility, denomination membership, count, and sum.   
    if count == -1:
        assert (
            coin_list is None
        ), f"Expected None list for impossible case (D={coins}, A={amount})"
        return

    assert (
        coin_list is not None
    ), f"Missing coin list for feasible case (D={coins}, A={amount})"
    assert len(coin_list) == count, (
        f"Count mismatch: reported {count}, list has {len(coin_list)}"
    )
    assert sum(coin_list) == amount, f"Sum mismatch: sum({coin_list}) != {amount}"
    coin_set = set(coins)
    for c in coin_list:
        assert c in coin_set, f"Invalid coin {c} used; not in {coins}"


# ==============================================================================
# 3. HAND-CHECKABLE & RANDOMIZED CROSS-VALIDATION
# ==============================================================================


def run_validation_suite() -> None:
    # 12 Hand-Checkable Test Cases
    hand_tests = [
        ([1, 5, 10, 25], 0, 0, "Amount requested is 0"),
        ([2, 5], 0, 0, "Amount requested is 0 with some values that aren't US coin values"),
        ([2, 4, 6], 7, -1, "Impossible odd target from even coins"),
        ([5, 10], 3, -1, "Impossible target smaller than smallest coin"),
        ([4, 7], 9, -1, "Values will never get to amount requested"),
        ([1, 3, 4], 6, 2, "Multiple optimal / classic greedy trap (3+3)"),
        ([2, 3, 4], 6, 2, "Multiple optimal solutions (3+3 or 4+2)"),
        ([1, 2, 5], 11, 3, "Similar to US currency"),
        ([1, 5, 6, 9], 11, 2, "6+5 vs greedy 9+1+1"),
        ([7], 21, 3, "The amount requested is a product of the given value"),
        ([3], 20, -1, "The amount requested is not a product of the given value"),
        ([1, 10, 25], 30, 3, "10+10+10 vs 25+1*5"),
    ]

    print("--- Running 12 Hand-Checkable Test Cases ---")
    for coins, amount, expected, desc in hand_tests:
        c_naive = coin_change_naive(coins, amount)
        c_memo = coin_change_memo(coins, amount)
        c_dp, list_dp = coin_change_dp(coins, amount)

        assert c_naive == c_memo == c_dp == expected, (
            f"Disagreement on '{desc}': naive={c_naive}, memo={c_memo}, dp={c_dp}, expected={expected}"
        )
        validate_solution(coins, amount, c_dp, list_dp)
    print("All 12 hand-checkable tests passed and validated.\n")

    # 150 Randomized Small Instances
    print("--- Running 150 Randomized Small Instances ---")
    random.seed(4050)
    for trial in range(150):
        k = random.randint(2, 5)
        coins = sorted(random.sample(range(1, 15), k))
        amount = random.randint(0, 22)

        c_naive = coin_change_naive(coins, amount)
        c_memo = coin_change_memo(coins, amount)
        c_dp, list_dp = coin_change_dp(coins, amount)

        assert c_naive == c_memo == c_dp, (
            f"Trial {trial} mismatch on D={coins}, A={amount}: "
            f"naive={c_naive}, memo={c_memo}, dp={c_dp}"
        )
        validate_solution(coins, amount, c_dp, list_dp)
    print(
        "All 150 randomized small tests agreed across all 3 solvers and passed validation.\n"
    )


# ==============================================================================
# 4. AUTOMATED GREEDY COUNTEREXAMPLE SEARCH
# ==============================================================================


def search_greedy_counterexamples(max_coin: int = 15, max_amount: int = 3) -> List[dict]:
    #Systematically searches small denomination sets D where greedy succeeds

    #but uses strictly more coins than DP.
        
    counterexamples = []

    for c2 in range(2, max_coin):
        for c3 in range(c2 + 1, max_coin + 1):
            coins = [1, c2, c3]
            for amount in range(1, max_amount + 1):
                dp_count, dp_list = coin_change_dp(coins, amount)
                gr_count, gr_list = coin_change_greedy(coins, amount)

                validate_solution(coins, amount, dp_count, dp_list)
                validate_solution(coins, amount, gr_count, gr_list)

                if gr_count != -1 and gr_count > dp_count:
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

# ==============================================================================
# 5. CSV EXPORT FOR DISTINCT COUNTEREXAMPLES
# ==============================================================================


def export_distinct_counterexamples_csv(
    counterexamples: List[dict],
    filename: str = "greedy_counterexamples.csv",
    limit: int = 3,
) -> List[dict]:
    #Filters for counterexamples with distinct coin systems D (ensuring the
    #required sanity check D=[1, 3, 4], A=6 is included) and writes them to CSV.
        
    distinct_examples = []
    seen_systems = set()

    # Prioritize the required sanity check D=[1, 3, 4], A=6 first
    for item in counterexamples:
        if item["D"] == [1, 3, 4] and item["A"] == 6:
            distinct_examples.append(item)
            seen_systems.add(tuple(item["D"]))
            break

    # Collect additional counterexamples with distinct denomination sets D
    for item in counterexamples:
        if len(distinct_examples) >= limit:
            break
        d_tuple = tuple(item["D"])
        if d_tuple not in seen_systems:
            distinct_examples.append(item)
            seen_systems.add(d_tuple)

    # Write selected counterexamples to CSV
    fieldnames = [
        "coin_system_D",
        "target_A",
        "greedy_count",
        "greedy_coins",
        "optimal_dp_count",
        "optimal_dp_coins",
        "extra_coins_used",
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for ex in distinct_examples:
            writer.writerow({
                "coin_system_D": str(ex["D"]),
                "target_A": ex["A"],
                "greedy_count": ex["greedy_count"],
                "greedy_coins": str(ex["greedy_coins"]),
                "optimal_dp_count": ex["opt_count"],
                "optimal_dp_coins": str(ex["opt_coins"]),
                "extra_coins_used": ex["gap"],
            })

    return distinct_examples