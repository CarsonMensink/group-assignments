import random
import io
from contextlib import redirect_stdout


def generate_random_instance(min_jobs=4, max_jobs=10):
    """Generate a random set of intervals."""
    n = random.randint(min_jobs, max_jobs)

    starts = []
    finishes = []

    for _ in range(n):
        start = random.randint(0, 20)
        duration = random.randint(1, 8)
        finish = start + duration

        starts.append(start)
        finishes.append(finish)

    return starts, finishes


def run_quietly(algorithm, n, starts, finishes):
    """Run a greedy algorithm without printing its normal output."""
    with redirect_stdout(io.StringIO()):
        return algorithm(n, starts, finishes)


def print_instance(starts, finishes):
    """Print every interval with its original job index."""
    print("Input intervals:")
    for i in range(len(starts)):
        print(f"  Job {i}: [{starts[i]}, {finishes[i]})")


def print_selection(label, selected_jobs, starts, finishes):
    """Print the intervals selected by an algorithm."""
    print(f"{label}:")
    for i in selected_jobs:
        print(f"  Job {i}: [{starts[i]}, {finishes[i]})")
    print(f"  Total selected: {len(selected_jobs)}")


def print_timeline(starts, finishes, selected_jobs):
    """Print a simple timeline for one counterexample."""
    print("\nTimeline (* = selected by the greedy algorithm):")

    selected = set(selected_jobs)

    for i in range(len(starts)):
        marker = "*" if i in selected else " "
        print(
            f"{marker} Job {i}: "
            f"{starts[i]:>2} -- {finishes[i]:>2}"
        )


def find_counterexample(
    algorithm_name,
    algorithm,
    optimal_solution,
    max_attempts=5000,
    min_jobs=4,
    max_jobs=10
):
    """
    Search random instances until the greedy algorithm selects
    fewer jobs than the exact solver, or the attempt limit is reached.
    """
    for attempt in range(1, max_attempts + 1):
        starts, finishes = generate_random_instance(
            min_jobs=min_jobs,
            max_jobs=max_jobs
        )
        n = len(starts)

        greedy_jobs = run_quietly(
            algorithm, n, starts, finishes
        )
        optimal_jobs = optimal_solution(n, starts, finishes)

        if len(greedy_jobs) < len(optimal_jobs):
            print("\n" + "=" * 60)
            print(f"Counterexample found: {algorithm_name}")
            print(f"Random attempts: {attempt}")
            print("=" * 60)

            print_instance(starts, finishes)
            print()
            print_selection(
                "Greedy solution", greedy_jobs, starts, finishes
            )
            print()
            print_selection(
                "Optimal solution", optimal_jobs, starts, finishes
            )

            print(
                f"\nDifference: the optimal solution selects "
                f"{len(optimal_jobs) - len(greedy_jobs)} "
                f"more job(s)."
            )

            print_timeline(starts, finishes, greedy_jobs)

            return {
                "algorithm": algorithm_name,
                "starts": starts,
                "finishes": finishes,
                "greedy_jobs": greedy_jobs,
                "optimal_jobs": optimal_jobs,
                "attempts": attempt
            }

    print(
        f"\nNo counterexample found for {algorithm_name} "
        f"after {max_attempts} attempts."
    )
    return None


def test_earliest_finish(
    earliest_finish_time,
    optimal_solution,
    number_of_tests=100
):
    """Verify Earliest Finish matches the exact solver on random cases."""
    print("\n" + "=" * 60)
    print("Earliest Finish validation")
    print("=" * 60)

    for test_number in range(1, number_of_tests + 1):
        starts, finishes = generate_random_instance(
            min_jobs=1,
            max_jobs=10
        )
        n = len(starts)

        greedy_jobs = run_quietly(
            earliest_finish_time, n, starts, finishes
        )
        optimal_jobs = optimal_solution(n, starts, finishes)

        if len(greedy_jobs) != len(optimal_jobs):
            print(f"FAILED on random test {test_number}")
            print_instance(starts, finishes)
            print_selection(
                "Earliest Finish", greedy_jobs, starts, finishes
            )
            print_selection(
                "Optimal solution", optimal_jobs, starts, finishes
            )
            return False

    print(
        f"PASSED: Earliest Finish matched the exact solver "
        f"on all {number_of_tests} random instances."
    )
    return True


def run_automated_search(
    earliest_finish_time,
    earliest_start_time,
    shortest_duration,
    custom_heuristic,
    optimal_solution
):
    """Search for greedy counterexamples and validate Earliest Finish."""
    random.seed()  # Use a new random seed for each program run.

    find_counterexample(
        "Earliest Start",
        earliest_start_time,
        optimal_solution
    )

    find_counterexample(
        "Shortest Duration",
        shortest_duration,
        optimal_solution
    )

    find_counterexample(
        "Custom Heuristic",
        custom_heuristic,
        optimal_solution
    )

    test_earliest_finish(
        earliest_finish_time,
        optimal_solution,
        number_of_tests=100
    )
