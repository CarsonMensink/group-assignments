import sys
from pathlib import Path

# Find Part 1 and Part 2 folders.
project_folder = Path(__file__).resolve().parent.parent
part1_folder = project_folder / "part-1"
part2_folder = project_folder / "part-2"

# Allow Python to import files from those folders.
sys.path.insert(0, str(part1_folder))
sys.path.insert(0, str(part2_folder))

from algorithms import earliest_finish_time, earliest_start_time, shortest_duration, longest_duartion
from optimal_solution import optimal_solution

from counter_examples import run_automated_search


def run_sanity_test(
    name,
    starts,
    finishes,
    greedy_algorithm,
    expected_greedy_count,
    expected_optimal_count,
    expected_greedy_jobs
):
    n = len(starts)

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    greedy_jobs = greedy_algorithm(n, starts, finishes)
    optimal_jobs = optimal_solution(n, starts, finishes)

    greedy_pass = (
        len(greedy_jobs) == expected_greedy_count
        and greedy_jobs == expected_greedy_jobs
    )
    optimal_pass = len(optimal_jobs) == expected_optimal_count

    print("Greedy job indices:", greedy_jobs)
    print("Optimal job indices:", optimal_jobs)
    print("Greedy count:", len(greedy_jobs))
    print("Optimal count:", len(optimal_jobs))

    passed = greedy_pass and optimal_pass
    print("SANITY TEST PASSED" if passed else "SANITY TEST FAILED")

    return passed


def run_required_sanity_tests():
    """Run the two required examples before searching randomly."""
    starts1 = [0, 1, 2, 3, 4]
    finishes1 = [10, 2, 3, 4, 5]

    test1_passed = run_sanity_test(
        name="Sanity Test 1: Earliest Start",
        starts=starts1,
        finishes=finishes1,
        greedy_algorithm=earliest_start_time,
        expected_greedy_count=1,
        expected_optimal_count=4,
        expected_greedy_jobs=[0]
    )

    starts2 = [2, 0, 3]
    finishes2 = [4, 3, 6]

    test2_passed = run_sanity_test(
        name="Sanity Test 2: Shortest Duration",
        starts=starts2,
        finishes=finishes2,
        greedy_algorithm=shortest_duration,
        expected_greedy_count=1,
        expected_optimal_count=2,
        expected_greedy_jobs=[0]
    )

    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("Both required sanity tests passed!")
    else:
        print("A sanity test failed. Fix it before continuing.")
    print("=" * 50)

    return test1_passed and test2_passed


def main():
    # Stop if the required sanity checks fail.
    if not run_required_sanity_tests():
        return

    # Search for counterexamples and run the 100-test validation.
    run_automated_search(
        earliest_finish_time=earliest_finish_time,
        earliest_start_time=earliest_start_time,
        shortest_duration=shortest_duration,
        custom_heuristic=longest_duartion,
        optimal_solution=optimal_solution
    )


if __name__ == "__main__":
    main()