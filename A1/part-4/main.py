import json
import os
import sys

# Direct runs need the assignment root on the import path for shared modules.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.greedy_algorithms import earliest_finish_time
from algorithms.optimal_algorithm import optimal_solution
from utils import compare_test, generate_tests, save_to_csv


def run_part_4():
    # Part 4 validates Earliest Finish against the exact solver across generated cases.
    print("\n" + "=" * 60)
    print("Part 4: Validate Earliest Finish")
    print("=" * 60)

    tests = generate_tests()
    results = []

    # Run solvers without console output so batch validation stays focused on its summary.
    for instance_id, dist_name, jobs in tests:
        greedy_solution = earliest_finish_time(jobs)
        exact_solution = optimal_solution(jobs)
        results.append(compare_test(instance_id, dist_name, jobs, greedy_solution, exact_solution))

    # Store nested interval and selection values as JSON so CSV readers can recover them.
    headers = [
        'Instance_ID', 'Distribution_Type', 'Intervals',
        'Earliest_Finish_Selected', 'OPT_Selected',
        'Earliest_Finish_Size', 'OPT_Size', 'Match',
    ]
    rows = [
        (
            result['Instance_ID'],
            result['Distribution_Type'],
            json.dumps(result['Intervals']),
            json.dumps(result['Earliest_Finish_Selected']),
            json.dumps(result['OPT_Selected']),
            result['Earliest_Finish_Size'],
            result['OPT_Size'],
            result['Match'],
        )
        for result in results
    ]

    # Save every case before reporting the aggregate match rate.
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "part4_validation_results.csv")
    save_to_csv(csv_path, headers, rows)

    # Report the validation summary so the result is visible without opening the CSV.
    matches = sum(result['Match'] for result in results)
    print(f"Earliest Finish matched OPT: {matches}/{len(results)} ({matches / len(results):.1%})")
    print("Results saved to CSV in part-4/ folder")


if __name__ == "__main__":
    run_part_4()
