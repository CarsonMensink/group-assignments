from typing import List

from jobs import Job

# This logic is shared across earliest start and earliest finish greedy functions
def select_forward_jobs(jobs: List[Job]) -> List[int]:
    # Allow the first job through while enforcing compatibility for every later job.
    prior_finish_time = float('-inf')
    selected_jobs = []

    # Accept touching endpoints because the assignment uses half-open intervals.
    for job in jobs:
        if job.start >= prior_finish_time:
            selected_jobs.append(job.index)
            prior_finish_time = job.finish

    return selected_jobs


def select_non_overlapping_jobs(jobs: List[Job]) -> List[int]:
    # Keep full records because duration order can select later intervals before earlier ones.
    selected_jobs: List[Job] = []

    # Accept a candidate only if it fits before or after every selected interval: O(n²).
    for candidate in jobs:
        if all(
            candidate.finish <= selected.start or candidate.start >= selected.finish
            for selected in selected_jobs
        ):
            selected_jobs.append(candidate)

    # Return original input identifiers so callers can report selections consistently.
    return [job.index for job in selected_jobs]


def earliest_finish_time(jobs: List[Job]) -> List[int]:
    # Earliest finish leaves the most room for compatible later jobs.
    jobs = sorted(jobs, key=lambda job: (job.finish, job.index))

    selected_jobs = select_forward_jobs(jobs)

    return selected_jobs


def earliest_start_time(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's earliest-start heuristic while using the shared job records.
    jobs = sorted(jobs, key=lambda job: (job.start, job.index))

    selected_jobs = select_forward_jobs(jobs)

    return selected_jobs

def shortest_duration(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's shortest-duration heuristic with the same input identifiers.
    jobs = sorted(jobs, key=lambda job: (job.finish - job.start, job.index))

    selected_jobs = select_non_overlapping_jobs(jobs)

    return selected_jobs

def longest_duration(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's longest-duration heuristic with deterministic tie-breaking.
    jobs = sorted(jobs, key=lambda job: (-(job.finish - job.start), job.index))

    selected_jobs = select_non_overlapping_jobs(jobs)

    return selected_jobs
