import csv
import os
import random
import sys

# part-1 sits next to part-4 in A1/. Resolve the path from this file so the script
# works no matter which directory it is run from.
PART_1_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'part-1')
sys.path.append(PART_1_DIR)
from algorithms import earliest_finish_time

def exact_solver(jobs):
    """
    Brute-force Exact Solver using recursive backtracking.
    Evaluates all compatible subsets to find the optimal solution.
    Practical only for small n (e.g., n <= 20).
    """
    jobs_sorted = sorted(jobs, key=lambda x: x[0])
    max_compatible = []

    def get_max_subset(idx, current_finish, current_subset):
        nonlocal max_compatible

        if idx == len(jobs_sorted):
            if len(current_subset) > len(max_compatible):
                max_compatible = current_subset[:]
            return

        # Branch 1: Exclude the current job
        get_max_subset(idx + 1, current_finish, current_subset)

        # Branch 2: Include the current job (if compatible)
        start, finish = jobs_sorted[idx]
        if start >= current_finish:
            current_subset.append(jobs_sorted[idx])
            get_max_subset(idx + 1, finish, current_subset)
            current_subset.pop() # Backtrack

    get_max_subset(0, -1, [])
    return max_compatible

# --- Distribution Generators (Timelines represented in Years AD) ---

def generate_sparse(n):
    """Short durations, spread out over a wide timeline."""
    return [(s := random.randint(100, 500), s + random.randint(1, 5)) for _ in range(n)]

def generate_heavily_overlapping(n):
    """Many intervals starting around the same time with long durations."""
    return [(s := random.randint(100, 120), s + random.randint(50, 100)) for _ in range(n)]

def generate_varied_lengths(n):
    """Mix of very short and very long intervals."""
    return [(s := random.randint(100, 300), s + random.choice([random.randint(1, 3), random.randint(50, 100)])) for _ in range(n)]

def generate_clustered_starts(n):
    """Starts grouped tightly around specific milestones (e.g., AD 100, AD 200, AD 300)."""
    clusters = [100, 200, 300]
    return [(s := random.choice(clusters) + random.randint(-5, 5), s + random.randint(10, 30)) for _ in range(n)]

def run_part_4_experiment():
    """Runs at least 100 instances across different distributions."""
    n_per_instance = 15 # Kept small so the exact solver remains practical
    total_instances = 100 # Minimum required by the assignment

    distributions = [
        ("Sparse", generate_sparse),
        ("Heavily Overlapping", generate_heavily_overlapping),
        ("Varied Lengths", generate_varied_lengths),
        ("Clustered Starts", generate_clustered_starts)
    ]

    matches = 0
    results_data = []

    print(f"Running Part 4 Validation: {total_instances} Instances (n={n_per_instance} jobs each)...\n")

    for i in range(total_instances):
        # Rotate evenly through the 4 distribution types
        dist_name, dist_func = distributions[i % len(distributions)]

        # Generate random jobs for this instance
        jobs = dist_func(n_per_instance)

        # Run Earliest Finish and Exact Solver
        # earliest_finish_time takes (n, start_times, finish_times) and returns selected indices
        starts = [s for s, _ in jobs]
        finishes = [f for _, f in jobs]
        greedy_solution = earliest_finish_time(len(jobs), starts, finishes)
        exact_solution = exact_solver(jobs)

        greedy_size = len(greedy_solution)
        opt_size = len(exact_solution)

        # Compare |EarliestFinish(I)| with OPT(I)
        is_match = (greedy_size == opt_size)
        if is_match:
            matches += 1

        results_data.append({
            'Instance_ID': i + 1,
            'Distribution_Type': dist_name,
            'Earliest_Finish_Size': greedy_size,
            'OPT_Size': opt_size,
            'Match': is_match
        })

    # Report Results
    print("-" * 50)
    print("EXPERIMENTAL RESULTS: Earliest Finish vs OPT")
    print("-" * 50)
    print(f"Total Instances Tested: {total_instances}")
    print(f"Matches (Earliest Finish == OPT): {matches}")
    print(f"Match Ratio: {matches}/{total_instances} ({(matches/total_instances)*100:.1f}%)")

    # Detailed check to ensure the distributions are varied
    print("\nBreakdown by Distribution Type:")
    for dist_name, _ in distributions:
        dist_matches = sum(1 for r in results_data if r['Distribution_Type'] == dist_name and r['Match'])
        dist_total = sum(1 for r in results_data if r['Distribution_Type'] == dist_name)
        print(f"  - {dist_name}: {dist_matches}/{dist_total} matches")

    # Export to CSV for machine-readable submission requirement
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Part4_Validation_Results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results_data[0].keys()))
        writer.writeheader()
        writer.writerows(results_data)
    print(f"\nMachine-readable experimental results exported to {csv_path}.")

if __name__ == "__main__":
    random.seed(2026)
    run_part_4_experiment()
