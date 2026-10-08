from utils import print_selected_jobs

from itertools import combinations

def optimal_solution(n, start_times, finish_times):
    best = []

    # try every possible subset size
    for size in range(n + 1):
        for combo in combinations(range(n), size):

            compatible = True

            # check every pair of jobs in this subset
            for i in range(len(combo)):
                for j in range(i + 1, len(combo)):
                    job1 = combo[i]
                    job2 = combo[j]

                    # jobs overlap
                    if (start_times[job1] < finish_times[job2] and
                        start_times[job2] < finish_times[job1]):
                        compatible = False
                        break

                if not compatible:
                    break

            if compatible and len(combo) > len(best):
                best = list(combo)

    print_selected_jobs("OPT", start_times, finish_times, best)
    return best