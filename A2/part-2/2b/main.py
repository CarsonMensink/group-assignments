import random
import csv
import sys
from pathlib import Path
from typing import List, Optional, TypedDict

# Allow this script to import the Part 2A algorithms module from the sibling folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2a"))

from algorithms import (
    coin_change_greedy,
    coin_change_naive,
    coin_change_memo,
    coin_change_dp,
)


# Counterexamples retain both solutions so the exported evidence can be checked independently.
class Counterexample(TypedDict):
    D: List[int]
    A: int
    greedy_count: int
    greedy_coins: List[int]
    opt_count: int
    opt_coins: List[int]
    gap: int


# ==============================================================================
# INDEPENDENT SOLUTION VALIDATOR
# ==============================================================================

def validate_solution(coins: List[int], amount: int, count: int, coin_list: Optional[List[int]]) -> None:
    # Valid results must match the target and count using only allowed denominations.
    if count == -1:
        assert coin_list is None, f"Expected None list for impossible case (D={coins}, A={amount})"
        return

    assert count >= 0, f"Invalid coin count {count} (D={coins}, A={amount})"
    assert coin_list is not None, f"Missing coin list for feasible case (D={coins}, A={amount})"
    assert len(coin_list) == count, f"Count mismatch: reported {count}, list has {len(coin_list)}"
    assert sum(coin_list) == amount, f"Sum mismatch: sum({coin_list}) != {amount}"

    coin_set = set(coins)
    for c in coin_list:
        assert c in coin_set, f"Invalid coin {c} used; not in {coins}"


# ==============================================================================
# VALIDATION SUITE & TEST RUNNER
# ==============================================================================

def compare_exact_solvers(coins: List[int], amount: int) -> int:
    # Arrange: exact methods must agree on the count, while equally good coin lists may differ.
    solvers = (coin_change_naive, coin_change_memo, coin_change_dp)

    # Act: use the shared Part 2A interface to collect each method's reconstructed solution.
    results = [solver(coins, amount) for solver in solvers]

    # Assert: independent list checks catch invalid solutions even when reported counts agree.
    for count, chosen in results:
        validate_solution(coins, amount, count, chosen)
    counts = [count for count, _ in results]
    assert counts[0] == counts[1] == counts[2], (
        f"Exact solvers disagree for D={coins}, A={amount}: "
        f"naive={counts[0]}, memo={counts[1]}, dp={counts[2]}"
    )
    return counts[0]


def run_validation_suite() -> None:
    # Arrange: hand-counted cases cover zero, impossibility, greedy traps, and alternative optima.
    hand_tests = [
        ([1, 5, 10, 25], 0, 0, "Amount requested is 0"),
        ([2, 5], 0, 0, "Zero target without denomination 1"),
        ([2, 4, 6], 7, -1, "Impossible odd target from even coins"),
        ([5, 10], 3, -1, "Impossible target smaller than smallest coin"),
        ([4, 7], 9, -1, "Impossible despite relatively prime denominations"),
        ([1, 3, 4], 6, 2, "Classic greedy trap (3+3)"),
        ([2, 3, 4], 6, 2, "Multiple optimal solutions (3+3 or 4+2)"),
        ([1, 2, 5], 11, 3, "Similar to US currency"),
        ([1, 5, 6, 9], 11, 2, "6+5 vs greedy 9+1+1"),
        ([7], 21, 3, "Single denomination forms target exactly"),
        ([3], 20, -1, "Single denomination cannot form target"),
        ([1, 10, 25], 30, 3, "10+10+10 beats greedy 25+1+1+1+1+1"),
    ]

    print(f"--- Running {len(hand_tests)} Hand-Checkable Test Cases ---")
    for coins, amount, expected, desc in hand_tests:
        # Act & Assert: every exact method must match the independently hand-counted answer.
        count = compare_exact_solvers(coins, amount)
        assert count == expected, f"Disagreement on '{desc}': got {count}, expected {expected}"
    print(f"All {len(hand_tests)} hand tests passed across all 3 exact solvers.\n")

    # Arrange: a local seed reproduces all 150 cases; small targets keep naive recursion practical.
    seed = 4050
    rng = random.Random(seed)
    trials = 150
    print(f"--- Running {trials} Randomized Small Instances (seed={seed}) ---")
    for trial in range(trials):
        coins = [1] + sorted(rng.sample(range(2, 15), rng.randint(1, 4)))
        amount = rng.randint(0, 22)

        # Act & Assert: coin 1 guarantees feasibility as well as an exact-count agreement check.
        count = compare_exact_solvers(coins, amount)
        assert count >= 0, f"Trial {trial}: D={coins}, A={amount} must be feasible with coin 1"
    print(f"All {trials} random tests passed across all 3 exact solvers.\n")


# ==============================================================================
# AUTOMATED GREEDY COUNTEREXAMPLE SEARCH & CSV EXPORT
# ==============================================================================

def search_greedy_counterexamples(max_coin: int = 15, max_amount: int = 25) -> List[Counterexample]:
    # Exhaustive small systems reveal feasible greedy solutions that use more coins than DP.
    counterexamples: List[Counterexample] = []
    for c2 in range(2, max_coin):
        for c3 in range(c2 + 1, max_coin + 1):
            coins = [1, c2, c3]
            for amount in range(1, max_amount + 1):
                dp_count, dp_list = coin_change_dp(coins, amount)
                gr_count, gr_list = coin_change_greedy(coins, amount)

                # Valid reconstructions are required before either result becomes search evidence.
                validate_solution(coins, amount, dp_count, dp_list)
                validate_solution(coins, amount, gr_count, gr_list)
                assert dp_count >= 0 and gr_count >= 0, f"Coin 1 must make D={coins}, A={amount} feasible"
                assert dp_list is not None and gr_list is not None
                if gr_count > dp_count:
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


def export_distinct_counterexamples(
    counterexamples: List[Counterexample], output_path: Path
) -> List[Counterexample]:
    # The required sanity example comes first, followed by two different denomination systems.
    sanity = [example for example in counterexamples if example["D"] == [1, 3, 4] and example["A"] == 6]
    assert len(sanity) == 1, "Search did not detect the required D=[1,3,4], A=6 counterexample"
    # The assignment's sanity check requires the stated solutions, not just a matching input.
    assert sanity[0]["greedy_count"] == 3 and sanity[0]["greedy_coins"] == [4, 1, 1], (
        "Required sanity case must give greedy 4+1+1 (3 coins)"
    )
    assert sanity[0]["opt_count"] == 2, "Required sanity case must have optimum 2 coins"
    selected = [sanity[0]]
    seen = {(1, 3, 4)}
    for example in counterexamples:
        system = tuple(example["D"])
        if system not in seen:
            selected.append(example)
            seen.add(system)
        if len(selected) == 3:
            break
    assert len(selected) == 3, "Search must provide at least 3 distinct counterexample systems"

    # Stable columns and order let teammates regenerate the CSV from any working directory.
    fieldnames = [
        "coin_system_D", "target_A", "greedy_count", "greedy_coins",
        "optimal_dp_count", "optimal_dp_coins", "extra_coins_used",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for example in selected:
            writer.writerow({
                "coin_system_D": example["D"],
                "target_A": example["A"],
                "greedy_count": example["greedy_count"],
                "greedy_coins": example["greedy_coins"],
                "optimal_dp_count": example["opt_count"],
                "optimal_dp_coins": example["opt_coins"],
                "extra_coins_used": example["gap"],
            })
    return selected


def main() -> None:
    # DP becomes the search oracle only after all exact methods pass cross-validation.
    run_validation_suite()
    examples = search_greedy_counterexamples()
    print(f"Found {len(examples)} greedy counterexamples (1 < c2 < c3 <= 15, 1 <= A <= 25).")
    output_path = Path(__file__).resolve().with_name("greedy_counterexamples.csv")
    selected = export_distinct_counterexamples(examples, output_path)
    print("Required sanity check passed: D=[1,3,4], A=6.")
    for example in selected:
        print(
            f"D={example['D']}, A={example['A']}: "
            f"greedy {example['greedy_coins']} ({example['greedy_count']}) vs "
            f"optimal {example['opt_coins']} ({example['opt_count']})"
        )
    print(f"Exported {len(selected)} distinct counterexamples to {output_path}")


if __name__ == "__main__":
    main()
