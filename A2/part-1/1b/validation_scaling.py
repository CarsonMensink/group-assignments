import random
import statistics
import time
from typing import List, Tuple


# ==========================================
# 1. Algorithms
# ==========================================

def count_inversions_brute_force(arr: List[int]) -> int:
    """O(n^2) brute-force inversion counter (small-instance oracle)."""
    n = len(arr)
    inversions = 0
    for i in range(n):
        ai = arr[i]
        for j in range(i + 1, n):
            if ai > arr[j]:
                inversions += 1
    return inversions


def count_inversions_divide_conquer(arr: List[int]) -> int:
    """O(n log n) divide-and-conquer inversion counter using merge sort."""
    working = list(arr)
    temp = [0] * len(working)

    def _merge_sort(left: int, right: int) -> int:
        if left >= right:
            return 0
        mid = (left + right) // 2
        inv = _merge_sort(left, mid)
        inv += _merge_sort(mid + 1, right)
        inv += _merge(left, mid, right)
        return inv

    def _merge(left: int, mid: int, right: int) -> int:
        i, j, k = left, mid + 1, left
        inv_count = 0

        while i <= mid and j <= right:
            if working[i] <= working[j]:
                temp[k] = working[i]
                i += 1
            else:
                temp[k] = working[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1

        while i <= mid:
            temp[k] = working[i]
            i += 1
            k += 1

        while j <= right:
            temp[k] = working[j]
            j += 1
            k += 1

        working[left : right + 1] = temp[left : right + 1]
        return inv_count

    return _merge_sort(0, len(working) - 1)


# ==========================================
# 2. Validation Suite (Oracle Testing)
# ==========================================

def run_validation(seed: int = 42) -> None:
    rng = random.Random(seed)

    hand_tests: List[Tuple[str, List[int], int]] = [
        ("Empty array", [], 0),
        ("Single element", [7], 0),
        ("Two elements sorted", [1, 2], 0),
        ("Two elements inverted", [2, 1], 1),
        ("Already sorted (n=6)", [1, 2, 3, 4, 5, 6], 0),
        ("Reverse sorted (n=5)", [5, 4, 3, 2, 1], 10),
        ("Nearly sorted (one adjacent swap)", [1, 3, 2, 4, 5], 1),
        ("Nearly sorted (end elements swapped)", [5, 2, 3, 4, 1], 7),
        ("All duplicates", [4, 4, 4, 4], 0),
        ("Sorted with duplicates", [1, 2, 2, 3, 3, 3], 0),
        ("Random small 1", [2, 4, 1, 3, 5], 3),
        ("Random small 2 (with negatives)", [-1, -5, 0, -2], 3),
    ]

    print("--- Running Hand-Checkable Validation Tests ---")
    for label, arr, expected in hand_tests:
        bf_res = count_inversions_brute_force(arr)
        dc_res = count_inversions_divide_conquer(arr)
        assert bf_res == expected, f"Oracle failed on '{label}': got {bf_res}, expected {expected}"
        assert dc_res == bf_res, f"Mismatch on '{label}': DC={dc_res}, BF={bf_res}"
    print(f"[PASS] All {len(hand_tests)} hand-crafted tests matched expected counts and oracle.")

    num_random_tests = 250
    print(f"--- Running {num_random_tests} Randomized Oracle Crosschecks ---")
    for test_idx in range(num_random_tests):
        size = rng.randint(0, 150)
        val_bound = 10 if test_idx % 3 == 0 else 10_000
        arr = [rng.randint(-val_bound, val_bound) for _ in range(size)]

        bf_res = count_inversions_brute_force(arr)
        dc_res = count_inversions_divide_conquer(arr)
        assert dc_res == bf_res, f"Randomized test #{test_idx} (n={size}) failed: DC={dc_res}, BF={bf_res}"
    print(f"[PASS] All {num_random_tests} random arrays matched exactly.\n")


# ==========================================
# 3. Fair Benchmarking & Detailed Statistics
# ==========================================

def compute_stats(times: List[float]) -> dict:
    """Computes median, min, max, and Interquartile Range (IQR) for dispersion analysis."""
    sorted_t = sorted(times)
    med = statistics.median(sorted_t)
    q1 = statistics.median(sorted_t[: len(sorted_t) // 2])
    q3 = statistics.median(sorted_t[(len(sorted_t) + 1) // 2 :])
    return {
        "min": sorted_t[0],
        "median": med,
        "max": sorted_t[-1],
        "iqr": q3 - q1,
    }


def benchmark_scaling(seed: int = 123) -> None:
    rng = random.Random(seed)
    sizes = [10, 25, 50, 75, 100, 150, 200, 300, 500, 1000, 2500, 5000, 10000]
    trials = 21  # Higher trial count for robust statistical distribution

    # Warm-up pass
    warmup_arr = [rng.randint(0, 1000) for _ in range(500)]
    count_inversions_brute_force(warmup_arr)
    count_inversions_divide_conquer(warmup_arr)

    print(f"{'n':>6} | {'Brute-Force (ms)':>30} | {'Divide & Conquer (ms)':>30} | {'Speedup':>10}")
    print(f"{'':>6} | {'Median':>9} {'IQR':>8} {'Min-Max':>10} | {'Median':>9} {'IQR':>8} {'Min-Max':>10} | {'(BF/DC)':>10}")
    print("-" * 84)

    crossover_n = None

    for n in sizes:
        datasets = [[rng.randint(-100_000, 100_000) for _ in range(n)] for _ in range(trials)]

        bf_times, dc_times = [], []

        for data in datasets:
            t0 = time.perf_counter()
            res_bf = count_inversions_brute_force(data)
            t1 = time.perf_counter()
            bf_times.append((t1 - t0) * 1000.0)

            t2 = time.perf_counter()
            res_dc = count_inversions_divide_conquer(data)
            t3 = time.perf_counter()
            dc_times.append((t3 - t2) * 1000.0)

            assert res_bf == res_dc

        bf_s = compute_stats(bf_times)
        dc_s = compute_stats(dc_times)
        speedup = bf_s["median"] / dc_s["median"] if dc_s["median"] > 0 else float("inf")

        if crossover_n is None and dc_s["median"] < bf_s["median"]:
            crossover_n = n

        bf_minmax = f"{bf_s['min']:.2f}-{bf_s['max']:.2f}"
        dc_minmax = f"{dc_s['min']:.2f}-{dc_s['max']:.2f}"

        print(
            f"{n:6d} | "
            f"{bf_s['median']:9.4f} {bf_s['iqr']:8.4f} {bf_minmax:>10} | "
            f"{dc_s['median']:9.4f} {dc_s['iqr']:8.4f} {dc_minmax:>10} | "
            f"{speedup:9.2f}x"
        )

    print("-" * 84)
    if crossover_n:
        print(f"\nStatistical Crossover Point: O(n log n) surpasses O(n^2) at n ≈ {crossover_n}.")


if __name__ == "__main__":
    run_validation()
    benchmark_scaling()