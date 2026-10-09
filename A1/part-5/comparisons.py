
import sys
import csv
import random
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
part1_folder = project_folder / "part-1"
part2_folder = project_folder / "part-2"

sys.path.insert(0, str(part1_folder))
sys.path.insert(0, str(part2_folder))

from algorithms import earliest_finish_time, earliest_start_time, shortest_duration, longest_duartion
from optimal_solution import optimal_solution


def generate_instance(instance_type, rng):
    """Generate one small interval-scheduling instance"""

    n = rng.randint(6, 12)
    starts = []
    finishes = []

    for _ in range(n):
        if instance_type == "sparse":
            # Short intervals spread across a wide range of times
            start = rng.randint(0, 100)
            duration = rng.randint(1, 4)

        elif instance_type == "overlapping":
            # Most intervals start near the same time
            start = rng.randint(0, 10)
            duration = rng.randint(8, 20)

        elif instance_type == "varied_lengths":
            # Mix very short and very long intervals
            start = rng.randint(0, 40)
            duration = rng.choice([1, 2, 3, 5, 10, 20, 30])

        else:  # clustered start times
            # Starts are concentrated around a few time points
            center = rng.choice([10, 30, 50])
            start = max(0, center + rng.randint(-3, 3))
            duration = rng.randint(1, 15)

        starts.append(start)
        finishes.append(start + duration)

    return starts, finishes


def describe_jobs(job_indices, starts, finishes):
    """Convert selected job indices into readable intervals"""
    return [
        (job, starts[job], finishes[job])
        for job in job_indices
    ]


def run_comparison():
    """Compare all four greedy algorithms against the exact solver"""

    number_of_instances = 120
    rng = random.Random(4050)

    heuristics = {
        "Earliest Finish": earliest_finish_time,
        "Earliest Start": earliest_start_time,
        "Shortest Duration": shortest_duration,
        "Longest Duration": longest_duartion
    }

    instance_types = [
        "sparse",
        "overlapping",
        "varied_lengths",
        "clustered"
    ]

    # Add results to CSV
    output_folder = Path(__file__).resolve().parent
    detailed_results_path = output_folder / "comparison_results.csv"
    summary_results_path = output_folder / "comparison_summary.csv"

    detailed_rows = []
    statistics = {
        name: {
            "optimal_count": 0,
            "quality_total": 0.0,
            "worst_ratio": float("inf"),
            "worst_instance": None
        }
        for name in heuristics
    }

    # Generate and evaluate 120 instances, 30 of each
    for instance_number in range(number_of_instances):
        instance_type = instance_types[
            instance_number % len(instance_types)
        ]

        starts, finishes = generate_instance(instance_type, rng)
        n = len(starts)

        optimal_jobs = optimal_solution(n, starts, finishes)
        optimal_count = len(optimal_jobs)

        if optimal_count == 0:
            raise ValueError(
                "The exact solver returned an empty solution "
                "for a nonempty valid instance."
            )

        for heuristic_name, heuristic in heuristics.items():
            selected_jobs = heuristic(n, starts, finishes)
            selected_count = len(selected_jobs)

            # Selected jobs / optimal jobs
            quality = selected_count / optimal_count
            is_optimal = selected_count == optimal_count

            stats = statistics[heuristic_name]

            if is_optimal:
                stats["optimal_count"] += 1

            stats["quality_total"] += quality

            # Save the lowest-quality instance
            if quality < stats["worst_ratio"]:
                stats["worst_ratio"] = quality
                stats["worst_instance"] = {
                    "instance_number": instance_number + 1,
                    "instance_type": instance_type,
                    "starts": starts[:],
                    "finishes": finishes[:],
                    "selected_jobs": selected_jobs[:],
                    "optimal_jobs": optimal_jobs[:],
                    "selected_count": selected_count,
                    "optimal_count": optimal_count
                }

            detailed_rows.append({
                "instance": instance_number + 1,
                "instance_type": instance_type,
                "heuristic": heuristic_name,
                "starts": starts,
                "finishes": finishes,
                "selected_jobs": selected_jobs,
                "selected_count": selected_count,
                "optimal_jobs": optimal_jobs,
                "optimal_count": optimal_count,
                "quality": quality,
                "is_optimal": is_optimal
            })

    # Write results
    with open(
        detailed_results_path, "w", newline="", encoding="utf-8"
    ) as file:
        fieldnames = [
            "instance",
            "instance_type",
            "heuristic",
            "starts",
            "finishes",
            "selected_jobs",
            "selected_count",
            "optimal_jobs",
            "optimal_count",
            "quality",
            "is_optimal"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in detailed_rows:
            saved_row = row.copy()

            # Store lists as readable text in CSV
            for column in [
                "starts", "finishes", "selected_jobs", "optimal_jobs"
            ]:
                saved_row[column] = str(saved_row[column])

            writer.writerow(saved_row)

    # Print and save summary stats
    print(f"Instances tested: {number_of_instances}")
    print(f"Random seed: 4050")
    print("\n{:<20} {:>14} {:>16} {:>14}".format(
        "Heuristic",
        "Optimal (%)",
        "Average quality",
        "Worst quality"
    ))
    print("-" * 68)

    summary_rows = []

    for name, stats in statistics.items():
        optimal_percentage = (
            stats["optimal_count"] / number_of_instances * 100
        )
        average_quality = (
            stats["quality_total"] / number_of_instances
        )
        worst = stats["worst_instance"]

        print("{:<20} {:>13.2f}% {:>16.4f} {:>14.4f}".format(
            name,
            optimal_percentage,
            average_quality,
            stats["worst_ratio"]
        ))

        summary_rows.append({
            "heuristic": name,
            "instances_tested": number_of_instances,
            "optimal_instances": stats["optimal_count"],
            "optimal_percentage": optimal_percentage,
            "average_quality": average_quality,
            "worst_quality": stats["worst_ratio"],
            "worst_instance_number": worst["instance_number"],
            "worst_instance_type": worst["instance_type"],
            "worst_starts": str(worst["starts"]),
            "worst_finishes": str(worst["finishes"]),
            "worst_selected_jobs": str(worst["selected_jobs"]),
            "worst_selected_count": worst["selected_count"],
            "worst_optimal_jobs": str(worst["optimal_jobs"]),
            "worst_optimal_count": worst["optimal_count"]
        })

        print(f"\n{name}: worst observed instance")
        print("  Instance number:", worst["instance_number"])
        print("  Instance type:", worst["instance_type"])
        print("  All intervals:", list(zip(
            worst["starts"], worst["finishes"]
        )))
        print("  Selected jobs:", describe_jobs(
            worst["selected_jobs"],
            worst["starts"],
            worst["finishes"]
        ))
        print("  Optimal jobs:", describe_jobs(
            worst["optimal_jobs"],
            worst["starts"],
            worst["finishes"]
        ))
        print(
            f"  Solution size: {worst['selected_count']} / "
            f"{worst['optimal_count']}"
        )
        print(f"  Quality: {stats['worst_ratio']:.4f}")

    with open(
        summary_results_path, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=summary_rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\nExperiment complete.")

if __name__ == "__main__":
    run_comparison()