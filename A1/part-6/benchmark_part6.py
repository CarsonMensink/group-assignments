import csv
import random
import statistics
import time
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../part-1")
))

import algorithms

# Do not include printing thousands of jobs in the runtime measurements.
# The original algorithm implementations remain unchanged.
def do_not_print(*args):
    pass

algorithms.print_selected_jobs = do_not_print

SIZES = [100, 1000, 10000, 100000]
RUNS = 10
SEED = 4050

METHODS = [
    ("Earliest Finish", algorithms.earliest_finish_time),
    ("Earliest Start", algorithms.earliest_start_time),
    ("Shortest Duration", algorithms.shortest_duration),
    ("Longest Duration", algorithms.longest_duartion),  # Original function spelling
]


def generate_jobs(n, rng):
    # Use the same jobs for every algorithm at a given input size.
    starts = [rng.randint(0, n * 10) for _ in range(n)]
    finishes = [start + rng.randint(1, 100) for start in starts]
    return starts, finishes


def main():
    rng = random.Random(SEED)
    results = []
    print("Median runtime (milliseconds) over", RUNS, "runs")
    print("Jobs\t" + "\t".join(name for name, _ in METHODS))

    for n in SIZES:
        starts, finishes = generate_jobs(n, rng)
        medians = []
        for name, method in METHODS:
            # Warm-up excluded from recorded timings.
            method(n, starts, finishes)
            timings = []
            for _ in range(RUNS):
                begin = time.perf_counter()
                method(n, starts, finishes)
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
