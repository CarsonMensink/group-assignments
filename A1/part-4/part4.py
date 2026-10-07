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
    n_per_instance = 15 # Kept small (n=15) so the exact solver remains practical
    total_instances = 100
    
    distributions = [
        ("Sparse", generate_sparse),
        ("Heavily Overlapping", generate_heavily_overlapping),
        ("Varied Lengths", generate_varied_lengths),
        ("Clustered Starts", generate_clustered_starts)
    ]
    
    matches = 0
    results = []

    print(f"Running Part 4 Validation: {total_instances} Instances (n={n_per_instance} jobs each)...\n")

    for i in range(total_instances):
        # Rotate evenly through the 4 distribution types
        dist_name, dist_func = distributions[i % len(distributions)]
        
        # Generate random jobs for this instance
        jobs = dist_func(n_per_instance)
        
        # Run both algorithms
        greedy_solution = earliest_finish_time(jobs)
        exact_solution = exact_solver(jobs)
        
        greedy_size = len(greedy_solution)
        opt_size = len(exact_solution)
        
        # Compare
        is_match = (greedy_size == opt_size)
        if is_match:
            matches += 1
            
        results.append({
            'Instance': i + 1,
            'Type': dist_name,
            'Greedy_Size': greedy_size,
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
        dist_matches = sum(1 for r in results if r['Type'] == dist_name and r['Match'])
        dist_total = sum(1 for r in results if r['Type'] == dist_name)
        print(f"  - {dist_name}: {dist_matches}/{dist_total} matches")

if __name__ == "__main__":
    random.seed(2026) # Seeded for reproducible experimental results[cite: 1]
    run_part_4_experiment()