import csv
import random
from jobs import make_jobs


# --- Part 4 distribution generators ---

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
    """Starts grouped tightly around the milestones 100, 200, and 300."""
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


def save_to_csv(path, headers, rows):
    """Write a header and rows so each assignment part can save its own CSV format."""
    # A shared writer keeps file handling consistent while callers define their own columns.
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    return path
