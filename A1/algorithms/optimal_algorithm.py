from typing import List

from jobs import Job

from itertools import combinations

def optimal_solution(jobs: List[Job]):
    best = []

    # Exhaustively compare subsets because this solver provides the correctness reference.
    for size in range(len(jobs) + 1):
        for combo in combinations(range(len(jobs)), size):

            compatible = True

            # check every pair of jobs in this subset
            for i in range(len(combo)):
                for j in range(i + 1, len(combo)):
                    job1 = jobs[combo[i]]
                    job2 = jobs[combo[j]]

                    # Half-open intervals may touch at an endpoint without overlapping.
                    if (job1.start < job2.finish and
                        job2.start < job1.finish):
                        compatible = False
                        break

                if not compatible:
                    break

            if compatible and len(combo) > len(best):
                best = [jobs[position].index for position in combo]

    return best
