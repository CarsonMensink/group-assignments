import sys
from pathlib import Path

part_folder = Path(__file__).resolve().parent
project_folder = part_folder.parent

# Direct runs and the global launcher both need access to shared and part-local modules.
sys.path.insert(0, str(project_folder))
sys.path.insert(0, str(part_folder))

from algorithms.greedy_algorithms import (
    earliest_finish_time,
    earliest_start_time,
    longest_duration,
    shortest_duration,
)
from algorithms.optimal_algorithm import optimal_solution
from jobs import make_jobs

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
    # Compare both solvers on identical Job records while preserving original indices.
    jobs = make_jobs(zip(starts, finishes))
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    greedy_jobs = greedy_algorithm(jobs)
    optimal_jobs = optimal_solution(jobs)

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


def run_part_3():
    # Stop if the required sanity checks fail.
    if not run_required_sanity_tests():
        return

    # Search for counterexamples and run the 100-test validation.
    run_automated_search(
        earliest_finish_time=earliest_finish_time,
        earliest_start_time=earliest_start_time,
        shortest_duration=shortest_duration,
        custom_heuristic=longest_duration,
        optimal_solution=optimal_solution
    )


def main():
    # Keep Part 3 runnable directly as well as through the global menu.
    run_part_3()


if __name__ == "__main__":
    main()
