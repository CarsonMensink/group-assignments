import random
import io
import json
from pathlib import Path
from contextlib import redirect_stdout

from jobs import make_jobs
from utils import save_to_csv


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


def run_quietly(algorithm, starts, finishes):
    """Run a greedy algorithm on shared Job records without console noise."""
    jobs = make_jobs(zip(starts, finishes))
    with redirect_stdout(io.StringIO()):
        return algorithm(jobs)


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
        greedy_jobs = run_quietly(
            algorithm, starts, finishes
        )
        optimal_jobs = optimal_solution(make_jobs(zip(starts, finishes)))

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
        greedy_jobs = run_quietly(
            earliest_finish_time, starts, finishes
        )
        optimal_jobs = optimal_solution(make_jobs(zip(starts, finishes)))

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
    # Reproduce the same searches even after running other parts from the menu.
    seed = 4050
    max_attempts = 5000
    random.seed(seed)
    print(f"Random seed: {seed}")

    earliest_start_example = find_counterexample(
        "Earliest Start",
        earliest_start_time,
        optimal_solution,
        max_attempts=max_attempts
    )

    shortest_duration_example = find_counterexample(
        "Shortest Duration",
        shortest_duration,
        optimal_solution,
        max_attempts=max_attempts
    )

    custom_example = find_counterexample(
        "Longest Duration",
        custom_heuristic,
        optimal_solution,
        max_attempts=max_attempts
    )

    test_earliest_finish(
        earliest_finish_time,
        optimal_solution,
        number_of_tests=100
    )

    # Keep one readable row per heuristic, including searches that find no counterexample.
    headers = [
        "Algorithm", "Seed", "Counterexample_Found", "Attempts",
        "Input_Intervals", "Greedy_Selected_Jobs", "Optimal_Selected_Jobs",
        "Greedy_Count", "Optimal_Count",
    ]
    rows = []
    for name, example in [
        ("Earliest Start", earliest_start_example),
        ("Shortest Duration", shortest_duration_example),
        ("Longest Duration", custom_example),
    ]:
        if example is None:
            # Blank evidence fields distinguish an unsuccessful search from an empty schedule.
            rows.append((name, seed, False, max_attempts, "", "", "", "", ""))
            continue

        # JSON within cells preserves lists; each interval's position is its original job index.
        rows.append((
            name, seed, True, example["attempts"],
            json.dumps(list(zip(example["starts"], example["finishes"]))),
            json.dumps(example["greedy_jobs"]),
            json.dumps(example["optimal_jobs"]),
            len(example["greedy_jobs"]), len(example["optimal_jobs"]),
        ))

    # Use the shared writer so Part 3 produces results in the same format as the other parts.
    output_path = Path(__file__).resolve().parent / "counterexamples.csv"
    save_to_csv(output_path, headers, rows)
    print(f"Counterexamples saved to {output_path.name}")
