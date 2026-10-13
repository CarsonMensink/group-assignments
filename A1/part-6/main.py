import random
import statistics
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms import greedy_algorithms
from jobs import Job
from utils import save_to_csv

SIZES = [100, 1000, 10000, 100000]
RUNS = 10
SEED = 4050

METHODS = [
    ("Earliest Finish", greedy_algorithms.earliest_finish_time),
    ("Earliest Start", greedy_algorithms.earliest_start_time),
    ("Shortest Duration", greedy_algorithms.shortest_duration),
    ("Longest Duration", greedy_algorithms.longest_duration),
]


def generate_jobs(n, rng):
    # Use the same indexed job records for every algorithm at a given input size.
    return [
        Job(start := rng.randint(0, n * 10), start + rng.randint(1, 100), index)
        for index in range(n)
    ]


def run_part_6():
    # Compare algorithm runtimes on the same generated jobs at each input size.
    print("\n" + "=" * 60)
    print("Part 6: Runtime Experiment")
    print("=" * 60)

    rng = random.Random(SEED)
    results = []
    print("Median runtime (milliseconds) over", RUNS, "runs")
    print(f"{'Jobs':>8}  {'Algorithm':<20}  {'Median (ms)':>12}")

    # Generate one job set for each size: 100, 1,000, 10,000, and 100,000 jobs
    for n in SIZES:
        jobs = generate_jobs(n, rng)
        # Run each greedy algorithm on the same jobs for this size
        for name, method in METHODS:
            # Warm-up excluded from recorded timings.
            method(jobs)

            # Time 10 runs and keep the median of all 10
            timings = []
            for _ in range(RUNS):
                # Start timer
                begin = time.perf_counter()
                # Run the greedy algorithm
                method(jobs)
                # End timer
                elapsed_ms = (time.perf_counter() - begin) * 1000
                # Add result to timings array
                timings.append(elapsed_ms)
            # Take the median of the 10 timed runs
            median_ms = statistics.median(timings)
            # Record the median time for this algorithm at size n
            results.append((n, name, median_ms))
            print(f"{n:>8}  {name:<20}  {median_ms:>12.3f}", flush=True)

    # Keep benchmark output compatible with the shared CSV writer.
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "part6_results.csv")
    save_to_csv(
        csv_path,
        ["n", "algorithm", "median_ms"],
        ((n, name, f"{median_ms:.6f}") for n, name, median_ms in results),
    )
    print("Results saved to part6_results.csv")


def main():
    # Preserve direct execution of the Part 6 script.
    run_part_6()


if __name__ == "__main__":
    main()
