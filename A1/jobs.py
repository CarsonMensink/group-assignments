from typing import Iterable, List, NamedTuple, Tuple

# One scheduled interval, with its input position preserved for results.
class Job(NamedTuple):
    start: int
    finish: int
    index: int

# Takes in a list of (start, finish) tuples
# Returns a list of Job objects
def make_jobs(intervals: Iterable[Tuple[int, int]]) -> List[Job]:
    # Assign stable indices once so every algorithm can return the same input identifiers.
    jobs = [Job(start, finish, index) for index, (start, finish) in enumerate(intervals)]
    # Reject empty or reversed intervals; every job must satisfy start < finish.
    for job in jobs:
        if job.start >= job.finish:
            raise ValueError(f"Job {job.index} has start {job.start} >= finish {job.finish}; expected start < finish.")
    return jobs
