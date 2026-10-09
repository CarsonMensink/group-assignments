import csv
import random
import statistics
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms import greedy_algorithms
from jobs import Job

SIZES = [100, 1000, 10000, 100000]
RUNS = 10
SEED = 4050

METHODS = [
    ("Earliest Finish", greedy_algorithms.earliest_finish_time),
    ("Earliest Start", greedy_algorithms.earliest_start_time),
    ("Shortest Duration", greedy_algorithms.shortest_duration),
    ("Longest Duration", greedy_algorithms.longest_duration),  # Original function spelling
]


def generate_jobs(n, rng):
    # Use the same indexed job records for every algorithm at a given input size.
    return [
        Job(start := rng.randint(0, n * 10), start + rng.randint(1, 100), index)
        for index in range(n)
    ]


def main():
    rng = random.Random(SEED)
    results = []
    print("Median runtime (milliseconds) over", RUNS, "runs")
    print("Jobs\t" + "\t".join(name for name, _ in METHODS))

    for n in SIZES:
        jobs = generate_jobs(n, rng)
        medians = []
        for name, method in METHODS:
            # Warm-up excluded from recorded timings.
            method(jobs)
            timings = []
            for _ in range(RUNS):
                begin = time.perf_counter()
                method(jobs)
                elapsed_ms = (time.perf_counter() - begin) * 1000
                timings.append(elapsed_ms)
            median_ms = statistics.median(timings)
            medians.append(median_ms)
            results.append((n, name, median_ms))
        print(f"{n}\t" + "\t".join(f"{t:.3f}" for t in medians), flush=True)

    with open("part6_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "algorithm", "median_ms"])
        writer.writerows((n, name, f"{t:.6f}") for n, name, t in results)
    print("Results saved to part6_results.csv")


if __name__ == "__main__":
    main()
