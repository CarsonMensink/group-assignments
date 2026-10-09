from contextlib import redirect_stdout
from io import StringIO

from algorithms.greedy_algorithms import earliest_finish_time
from algorithms.optimal_algorithm import optimal_solution
from utils import compare_test, generate_tests, save_to_csv


def main():
    # compare Earliest Finish with OPT on every generated Part 4 test
    tests = generate_tests()
    results = []

    # the existing solvers print each selection show only the final summary here
    with redirect_stdout(StringIO()):
        for instance_id, dist_name, jobs in tests:
            starts = [start for start, _ in jobs]
            finishes = [finish for _, finish in jobs]

            greedy_solution = earliest_finish_time(len(jobs), starts, finishes)
            exact_solution = optimal_solution(len(jobs), starts, finishes)

            results.append(compare_test(instance_id, dist_name, jobs, greedy_solution, exact_solution))

    # write every case to CSV and summarize the matches in the terminal.
    save_to_csv(results)

    # print match rate in terminal
    matches = sum(result['Match'] for result in results)
    print(f"Earliest Finish matched OPT: {matches}/{len(results)} ({matches / len(results):.1%})")
    print("Results saved to CSV in part-4/ folder")

if __name__ == "__main__":
    main()
