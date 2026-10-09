import csv
import json
import os
import random
from typing import List
from jobs import Job, make_jobs


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

def generate_tests():
    """Return 100 reproducible test cases across the existing distributions."""
    random.seed(2026)
    n_per_instance = 15 # Kept small so the exact solver remains practical
    total_instances = 100 # Minimum required by the assignment

    distributions = [
        ("Sparse", generate_sparse),
        ("Heavily Overlapping", generate_heavily_overlapping),
        ("Varied Lengths", generate_varied_lengths),
        ("Clustered Starts", generate_clustered_starts)
    ]

    tests = []
    # Give each distribution 25 cases so the experiment covers different interval patterns.
    for i in range(total_instances):
        dist_name, dist_func = distributions[i % len(distributions)]
        jobs = make_jobs(dist_func(n_per_instance))
        tests.append((i + 1, dist_name, jobs))
    return tests


def compare_test(instance_id, dist_name, jobs, greedy_solution, exact_solution):
    """Return one record with the input, both selections, and whether their sizes match."""
    greedy_size = len(greedy_solution)
    opt_size = len(exact_solution)
    is_match = (greedy_size == opt_size)

    return {
        'Instance_ID': instance_id,
        'Distribution_Type': dist_name,
        'Intervals': [(job.start, job.finish) for job in jobs],
        'Earliest_Finish_Selected': greedy_solution,
        'OPT_Selected': exact_solution,
        'Earliest_Finish_Size': greedy_size,
        'OPT_Size': opt_size,
        'Match': is_match,
    }


def save_to_csv(results_data):
    """Overwrite the Part 4 CSV with one machine-readable row per test case."""
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "part-4", "part4_validation_results.csv")
    fieldnames = [
        'Instance_ID', 'Distribution_Type', 'Intervals',
        'Earliest_Finish_Selected', 'OPT_Selected',
        'Earliest_Finish_Size', 'OPT_Size', 'Match',
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Store interval and selection lists as JSON so CSV readers can recover them.
        for result in results_data:
            writer.writerow({
                **result,
                'Intervals': json.dumps(result['Intervals']),
                'Earliest_Finish_Selected': json.dumps(result['Earliest_Finish_Selected']),
                'OPT_Selected': json.dumps(result['OPT_Selected']),
            })
    return csv_path
