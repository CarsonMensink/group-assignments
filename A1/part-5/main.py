
import random
from pathlib import Path
import sys

part_folder = Path(__file__).resolve().parent
project_folder = part_folder.parent

# Direct runs need the assignment root for shared algorithms and utilities.
sys.path.insert(0, str(project_folder))

from algorithms.greedy_algorithms import (
    earliest_finish_time,
    earliest_start_time,
    longest_duration,
    shortest_duration,
)
from algorithms.optimal_algorithm import optimal_solution
from jobs import make_jobs
from utils import save_to_csv


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


def run_part_5():
    """Compare all four shared greedy algorithms against the exact solver."""
    # Identify this experiment clearly in output from both direct and menu runs.
    print("\n" + "=" * 60)
    print("Part 5: Compare Greedy Algorithms")
    print("=" * 60)

    number_of_instances = 120
    rng = random.Random(4050)

    heuristics = {
        "Earliest Finish": earliest_finish_time,
        "Earliest Start": earliest_start_time,
        "Shortest Duration": shortest_duration,
        "Longest Duration": longest_duration
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
        # Share indexed Job records so heuristic and exact results use the same input IDs.
        jobs = make_jobs(zip(starts, finishes))
        optimal_jobs = optimal_solution(jobs)
        optimal_count = len(optimal_jobs)

        if optimal_count == 0:
            raise ValueError(
                "The exact solver returned an empty solution "
                "for a nonempty valid instance."
            )

        for heuristic_name, heuristic in heuristics.items():
            selected_jobs = heuristic(jobs)
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

    # Keep detailed CSV columns stable while storing list fields as readable text.
    detailed_headers = [
        "instance", "instance_type", "heuristic", "starts", "finishes",
        "selected_jobs", "selected_count", "optimal_jobs", "optimal_count",
        "quality", "is_optimal",
    ]
    detailed_rows_for_csv = [
        (
            row["instance"], row["instance_type"], row["heuristic"],
            str(row["starts"]), str(row["finishes"]), str(row["selected_jobs"]),
            row["selected_count"], str(row["optimal_jobs"]),
            row["optimal_count"], row["quality"], row["is_optimal"],
        )
        for row in detailed_rows
    ]
    save_to_csv(detailed_results_path, detailed_headers, detailed_rows_for_csv)

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

    # Use the same CSV writer for the compact summary file.
    summary_headers = list(summary_rows[0].keys())
    summary_rows_for_csv = (
        tuple(row[header] for header in summary_headers)
        for row in summary_rows
    )
    save_to_csv(summary_results_path, summary_headers, summary_rows_for_csv)

    print("\nExperiment complete.")


def main():
    # Preserve standalone execution while sharing the same Part 5 runner as the menu.
    run_part_5()


if __name__ == "__main__":
    main()
