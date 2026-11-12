"""Part 1B validation: brute force is the oracle for divide and conquer.

Checks, for every validation array:
  1. brute_force_count(A) == sort_and_count(A)[0]
  2. the divide-and-conquer output equals sorted(A)
  3. neither function modified A
  4. for hand-checkable cases, both equal the count worked out by hand

Writes validation_results.csv beside this script.
"""

import csv
import random
import sys
from pathlib import Path

script_folder = Path(__file__).resolve().parent
sys.path.insert(0, str(script_folder.parent / "1a"))

from inversions import brute_force_count, sort_and_count  # noqa: E402

VALIDATION_SEED = 4050
RANDOM_DISTINCT_CASES = 300
RANDOM_DUPLICATE_CASES = 50
MAX_RANDOM_N = 60

# Each expected count was worked out by listing the inverted pairs by hand.
HAND_CASES = [
    ("empty", [], 0, "no pairs"),
    ("single", [7], 0, "no pairs"),
    ("two sorted", [10, 20], 0, "10<20"),
    ("two reversed", [20, 10], 1, "(20,10)"),
    ("already sorted", [1, 2, 3, 4, 5], 0, "every pair in order"),
    ("reverse sorted n=5", [5, 4, 3, 2, 1], 10, "all C(5,2)=10 pairs"),
    ("reverse sorted n=4", [8, 4, 2, 1], 6, "all C(4,2)=6 pairs"),
    ("nearly sorted: one adjacent swap", [1, 2, 4, 3, 5], 1, "(4,3)"),
    ("nearly sorted: two adjacent swaps", [2, 1, 3, 4, 6, 5], 2, "(2,1) (6,5)"),
    ("nearly sorted: one element moved right", [1, 5, 2, 3, 4], 3,
     "(5,2) (5,3) (5,4)"),
    ("largest first", [6, 1, 2, 3, 4, 5], 5, "6 before each of 1..5"),
    ("textbook example", [2, 4, 1, 3, 5], 3, "(2,1) (4,1) (4,3)"),
    ("small random", [3, 1, 2], 2, "(3,1) (3,2)"),
    ("random order", [3, 7, 1, 9, 5, 2], 8,
     "(3,1) (3,2) (7,1) (7,5) (7,2) (9,5) (9,2) (5,2)"),
    ("negative values", [-1, -5, 0, 3, -2], 4,
     "(-1,-5) (-1,-2) (0,-2) (3,-2)"),
]


def check_case(case_id, kind, arr, expected=None, pairs=""):
    """Run both counters on arr and return one result row."""

    original = list(arr)
    brute = brute_force_count(arr)
    dc_count, dc_sorted = sort_and_count(arr)

    agree = brute == dc_count
    sorted_ok = dc_sorted == sorted(original)
    unchanged = arr == original
    expected_ok = expected is None or (brute == expected and dc_count == expected)

    return {
        "case_id": case_id,
        "kind": kind,
        "n": len(arr),
        "array": " ".join(map(str, arr)) if len(arr) <= 20 else "",
        "expected": "" if expected is None else expected,
        "hand_pairs": pairs,
        "brute_force": brute,
        "divide_conquer": dc_count,
        "counts_agree": agree,
        "sorted_output_ok": sorted_ok,
        "input_unchanged": unchanged,
        "matches_expected": expected_ok,
        "passed": agree and sorted_ok and unchanged and expected_ok,
    }


def build_rows():
    rows = []
    case_id = 0

    for name, arr, expected, pairs in HAND_CASES:
        case_id += 1
        rows.append(check_case(case_id, f"hand: {name}", arr, expected, pairs))

    # Seeded so the same arrays are produced on every run.
    rng = random.Random(VALIDATION_SEED)

    # The assignment defines inversions on distinct values, so these are the
    # required randomized cross-checks.
    for _ in range(RANDOM_DISTINCT_CASES):
        case_id += 1
        n = rng.randint(0, MAX_RANDOM_N)
        arr = rng.sample(range(-1000, 1000), n)
        rows.append(check_case(case_id, "random distinct", arr))

    # Extra robustness check: equal values are not inversions (A[i] > A[j] is
    # strict), which the merge handles by taking from the left on ties.
    for _ in range(RANDOM_DUPLICATE_CASES):
        case_id += 1
        n = rng.randint(0, MAX_RANDOM_N)
        arr = [rng.randint(0, 9) for _ in range(n)]
        rows.append(check_case(case_id, "random with duplicates", arr))

    return rows


def run_validation():
    rows = build_rows()

    out_path = script_folder / "validation_results.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("Part 1B validation (brute force is the oracle)")
    print(f"  seed = {VALIDATION_SEED}")
    groups = {}
    for row in rows:
        group = "hand-checkable" if row["kind"].startswith("hand") else row["kind"]
        passed, total = groups.get(group, (0, 0))
        groups[group] = (passed + row["passed"], total + 1)
    for group, (passed, total) in groups.items():
        print(f"  {group:<24} {passed:>4} / {total:<4} passed")

    failures = [row for row in rows if not row["passed"]]
    for row in failures:
        print(f"  FAIL case {row['case_id']} ({row['kind']}): {row}")

    print(f"  wrote {out_path.name}")
    if failures:
        raise SystemExit(f"{len(failures)} validation case(s) failed")
    print("  [PASS] all validation arrays agree exactly\n")
    return rows


if __name__ == "__main__":
    run_validation()
