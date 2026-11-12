from exact_solver import (
    export_distinct_counterexamples_csv,
    inspect_dp_table,
    run_validation_suite,
    search_greedy_counterexamples,
)


def main() -> None:
    print("========================================================")
    print(" CMP_SC 4050 - Assignment 2: Coin Change Verification")
    print("========================================================\n")

    # 1. Run cross-validation suite (hand tests + 150 randomized tests)
    run_validation_suite()

    # 2. Run DP table trace demonstration on the required sanity check case
    inspect_dp_table([1, 3, 4], 6)

    # 3. Search for automated greedy counterexamples
    cex = search_greedy_counterexamples(max_coin=12, max_amount=25)
    print(
        f"\nFound {len(cex)} total greedy suboptimality instances in search space."
    )

    # 4. Verify required sanity check D = {1, 3, 4}, A = 6
    sanity = [x for x in cex if x["D"] == [1, 3, 4] and x["A"] == 6]
    assert len(sanity) == 1, "Sanity check D={1,3,4}, A=6 was not detected!"
    print("[PASS] Sanity check confirmed:", sanity[0])

    # 5. Export 3 distinct greedy counterexamples to CSV
    exported = export_distinct_counterexamples_csv(
        cex, filename="greedy_counterexamples.csv", limit=3
    )
    print(
        f"\n[PASS] Exported {len(exported)} distinct counterexamples to 'greedy_counterexamples.csv':"
    )
    for row in exported:
        print(
            f"  - D={row['D']}, A={row['A']} | Greedy: {row['greedy_coins']} ({row['greedy_count']}) vs DP: {row['opt_coins']} ({row['opt_count']})"
        )


if __name__ == "__main__":
    main()