from typing import List

from jobs import Job


def select_compatible_jobs(jobs: List[Job]) -> List[int]:
    # Store only actual endpoints so large gaps between times do not waste memory.
    endpoints = set()
    for job in jobs:
        endpoints.add(job.start)
        endpoints.add(job.finish)
    times = sorted(endpoints)

    # Fenwick trees use positions starting at 1; each tree counts selected endpoints.
    positions = {time: index for index, time in enumerate(times, start=1)}
    start_counts = [0] * (len(times) + 1)
    finish_counts = [0] * (len(times) + 1)
    selected_jobs: List[int] = []

    def count_through(tree: List[int], position: int) -> int:
        # Count selected endpoints up to this position in O(log n), without scanning jobs.
        total = 0
        # Each step adds a stored block, then skips it to avoid counting it twice.
        while position > 0:
            total += tree[position]
            position -= position & -position
        return total

    def record_endpoint(tree: List[int], position: int) -> None:
        # Keep endpoint counts ready for future overlap queries in O(log n).
        # Each step updates a larger stored block that includes this endpoint.
        while position < len(tree):
            tree[position] += 1
            position += position & -position

    # Keep the caller's priority order while allowing compatible jobs anywhere on the timeline.
    for job in jobs:
        start_position = positions[job.start]
        finish_position = positions[job.finish]

        # Exclude jobs starting at this finish and jobs ending at this start: touching is allowed.
        starts_before_finish = count_through(start_counts, finish_position - 1)
        finishes_by_start = count_through(finish_counts, start_position)
        overlaps = starts_before_finish - finishes_by_start
        if overlaps == 0:
            selected_jobs.append(job.index)
            record_endpoint(start_counts, start_position)
            record_endpoint(finish_counts, finish_position)

    return selected_jobs


def earliest_finish_time(jobs: List[Job]) -> List[int]:
    # Earliest finish leaves the most room for compatible later jobs.
    jobs = sorted(jobs, key=lambda job: (job.finish, job.index))

    return select_compatible_jobs(jobs)


def earliest_start_time(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's earliest-start heuristic while using the shared job records.
    jobs = sorted(jobs, key=lambda job: (job.start, job.index))

    return select_compatible_jobs(jobs)


def shortest_duration(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's shortest-duration heuristic with the same input identifiers.
    jobs = sorted(jobs, key=lambda job: (job.finish - job.start, job.index))

    return select_compatible_jobs(jobs)


def longest_duration(jobs: List[Job]) -> List[int]:
    # Preserve the assignment's longest-duration heuristic with deterministic tie-breaking.
    jobs = sorted(jobs, key=lambda job: (-(job.finish - job.start), job.index))

    return select_compatible_jobs(jobs)
