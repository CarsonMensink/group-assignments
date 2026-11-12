"""Part 1B runtime scaling: brute force vs divide and conquer.

Timing methodology
  - Every input is a seeded random permutation of 0..n-1 (distinct values),
    generated before any timing starts. Both algorithms get the same list.
  - Only the counter call is inside the timed region. Input generation,
    comparison counting, CSV writing, and plotting all happen outside it.
  - timeit runs with the garbage collector disabled. For each (algorithm, n),
    the loop count is calibrated so that one repetition lasts at least
    MIN_REPEAT_SECONDS, which keeps tiny inputs above timer resolution.
  - Each (algorithm, n) is measured REPEATS times; the median per-call time
    is the reported statistic (min and max are kept for spread).

Writes benchmark_results.csv (one row per algorithm and n) and
benchmark_raw.csv (every repetition) beside this script.
"""

import csv
import math
import platform
import random
import statistics
import sys
import timeit
from pathlib import Path

script_folder = Path(__file__).resolve().parent
sys.path.insert(0, str(script_folder.parent / "1a"))

from inversions import (  # noqa: E402
    brute_force_comparisons,
    brute_force_count,
    sort_and_count,
    sort_and_count_comparisons,
)

BENCHMARK_SEED = 2026
REPEATS = 7
MIN_REPEAT_SECONDS = 0.02

# Fine-grained small sizes locate the crossover; large sizes show growth.
SHARED_SIZES = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256,
                384, 512, 768, 1024, 1536, 2048, 3072, 4096]
BRUTE_ONLY_MAX = 8192          # brute force stops here (~1 s per call)
DC_EXTRA_SIZES = [8192, 16384, 32768, 65536, 131072, 262144]

ALGORITHMS = {
    "brute_force": lambda arr: brute_force_count(arr),
    "divide_conquer": lambda arr: sort_and_count(arr)[0],
}


def make_input(n, seed):
    rng = random.Random(seed * 1_000_003 + n)
    arr = list(range(n))
    rng.shuffle(arr)
    return arr


def calibrate(timer):
    """Smallest loop count (1, 2, 5, 10, 20, ...) that lasts MIN_REPEAT_SECONDS."""

    number = 1
    while True:
        for factor in (1, 2, 5):
            loops = number * factor
            if timer.timeit(loops) >= MIN_REPEAT_SECONDS:
                return loops
        number *= 10


def time_algorithm(func, arr):
    timer = timeit.Timer(lambda: func(arr))
    loops = calibrate(timer)
    totals = timer.repeat(repeat=REPEATS, number=loops)
    return loops, [total / loops for total in totals]


def run_benchmark():
    plan = [(n, ["brute_force", "divide_conquer"]) for n in SHARED_SIZES]
    for n in DC_EXTRA_SIZES:
        algs = ["divide_conquer"]
        if n <= BRUTE_ONLY_MAX:
            algs.insert(0, "brute_force")
        plan.append((n, algs))

    # Generate every input up front so no generation happens near timing.
    inputs = {n: make_input(n, BENCHMARK_SEED) for n, _ in plan}

    print("Part 1B runtime benchmark")
    print(f"  python {platform.python_version()} on {platform.machine()} "
          f"({platform.system()} {platform.release()})")
    print(f"  seed = {BENCHMARK_SEED}, repeats = {REPEATS}, statistic = median")
    print(f"  {'n':>7} {'algorithm':<15} {'median (s)':>12} {'loops':>7}")

    summary = []
    raw = []
    for n, algs in plan:
        arr = inputs[n]

        # Untimed: inversion counts and comparison counts for the report.
        dc_inv, dc_sorted, dc_cmp = sort_and_count_comparisons(arr)
        assert dc_sorted == sorted(arr)

        for name in algs:
            loops, per_call = time_algorithm(ALGORITHMS[name], arr)
            median = statistics.median(per_call)
            comparisons = (brute_force_comparisons(n) if name == "brute_force"
                           else dc_cmp)
            summary.append({
                "algorithm": name,
                "n": n,
                "inversions": dc_inv,
                "comparisons": comparisons,
                "repeats": REPEATS,
                "loops_per_repeat": loops,
                "median_s": median,
                "min_s": min(per_call),
                "max_s": max(per_call),
                "ns_per_n2": median / (n * n) * 1e9,
                "ns_per_nlog2n": median / (n * math.log2(n)) * 1e9,
            })
            for rep, seconds in enumerate(per_call, start=1):
                raw.append({"algorithm": name, "n": n, "repeat": rep,
                            "seconds_per_call": seconds})
            print(f"  {n:>7} {name:<15} {median:>12.3e} {loops:>7}")

        # Untimed cross-check on the benchmark inputs themselves.
        if "brute_force" in algs and n <= 2048:
            assert brute_force_count(arr) == dc_inv

    write_csv(script_folder / "benchmark_results.csv", summary)
    write_csv(script_folder / "benchmark_raw.csv", raw)
    print("  wrote benchmark_results.csv and benchmark_raw.csv")

    report_crossover(summary)
    return summary


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def report_crossover(summary):
    """Print the n after which divide and conquer is faster at every larger n."""

    brute = {r["n"]: r["median_s"] for r in summary if r["algorithm"] == "brute_force"}
    dc = {r["n"]: r["median_s"] for r in summary if r["algorithm"] == "divide_conquer"}
    shared = sorted(set(brute) & set(dc))

    crossover = None
    for index, n in enumerate(shared):
        if all(dc[m] < brute[m] for m in shared[index:]):
            crossover = n
            break

    print("\n  speedup = brute median / divide-and-conquer median")
    for n in shared:
        print(f"  n = {n:>5}: {brute[n] / dc[n]:8.2f}x")
    if crossover is None:
        print("  divide and conquer never stays ahead in the tested range")
    else:
        below = shared[shared.index(crossover) - 1] if crossover != shared[0] else None
        print(f"\n  crossover: divide and conquer is faster for every tested n >= "
              f"{crossover} (last n where brute force was not slower: {below})\n")


if __name__ == "__main__":
    run_benchmark()
