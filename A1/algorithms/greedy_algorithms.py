from typing import List

from jobs import Job

# This logic is shared across all greedy functions
def select_compatible_jobs(jobs):
    # Allow the first job through while enforcing compatibility for every later job.
    prior_finish_time = float('-inf')
    selected_jobs = []

    # Keep this scan shared so each ordering strategy applies identical interval rules.
    for job in jobs:
        if job.start >= prior_finish_time:
            selected_jobs.append(job.index)
            prior_finish_time = job.finish

    return selected_jobs

def earliest_finish_time(jobs: List[Job]):
    # Earliest finish leaves the most room for compatible later jobs.
    jobs = sorted(jobs, key=lambda job: (job.finish, job.index))

    selected_jobs = select_compatible_jobs(jobs)

    return selected_jobs


def earliest_start_time(jobs: List[Job]):
    # Preserve the assignment's earliest-start heuristic while using the shared job records.
    jobs = sorted(jobs, key=lambda job: (job.start, job.index))

    selected_jobs = select_compatible_jobs(jobs)

    return selected_jobs

def shortest_duration(jobs: List[Job]):
    # Preserve the assignment's shortest-duration heuristic with the same input identifiers.
    jobs = sorted(jobs, key=lambda job: (job.finish - job.start, job.index))

    selected_jobs = select_compatible_jobs(jobs)

    return selected_jobs

def longest_duartion(jobs: List[Job]):
    # Preserve the assignment's longest-duration heuristic with deterministic tie-breaking.
    jobs = sorted(jobs, key=lambda job: (-(job.finish - job.start), job.index))

    selected_jobs = select_compatible_jobs(jobs)

    return selected_jobs
