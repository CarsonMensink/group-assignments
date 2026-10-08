from utils import print_selected_jobs

# This logic is shared across all greedy functions
def select_compatible_jobs(jobs):
    # right away the first start time should be >= no matter what, so we set to -inf
    prior_finish_time = float('-inf')
    selected_jobs = []

    # loop through the sorted jobs
    # this unpacks the tuple for each job
    for start_time, finish_time, original_index in jobs:
        if start_time >= prior_finish_time:
            selected_jobs.append(original_index)
            prior_finish_time = finish_time

    return selected_jobs

def earliest_finish_time(n, start_times, finish_times):
    # put start times and finish times with their index together in a list of tuples
    jobs = [
        (start_times[i], finish_times[i], i)
        for i in range(n)
    ]

    # sort jobs by earliest finish time first
    # ties are broken by the earlier original index
    jobs.sort(key=lambda job: (job[1], job[2]))

    selected_jobs = select_compatible_jobs(jobs)

    print_selected_jobs("Earliest Finish Time", start_times, finish_times, selected_jobs)
    return selected_jobs


def earliest_start_time(n, start_times, finish_times):
    # put start times and finish times with their index together in a list of tuples
    jobs = [
        (start_times[i], finish_times[i], i)
        for i in range(n)
    ]

    # sort jobs by earliest start time first
    # ties are broken by the earlier original index
    jobs.sort(key=lambda job: (job[0], job[2]))

    selected_jobs = select_compatible_jobs(jobs)

    print_selected_jobs("Earliest Start Time", start_times, finish_times, selected_jobs)
    return selected_jobs

def shortest_duration(n, start_times, finish_times):
    # put start times and finish times with their index together in a list of tuples
    jobs = [
        (start_times[i], finish_times[i], i)
        for i in range(n)
    ]

    # sort jobs by shortest duration first
    # ties are broken by the earlier original index
    jobs.sort(key=lambda job: (job[1] - job[0], job[2]))

    selected_jobs = select_compatible_jobs(jobs)

    print_selected_jobs("Shortest Duration", start_times, finish_times, selected_jobs)
    return selected_jobs

def longest_duartion(n, start_times, finish_times):
    # put start times and finish times with their index together in a list of tuples
    jobs = [
        (start_times[i], finish_times[i], i)
        for i in range(n)
    ]

    # sort jobs by longest duration first
    # ties are broken by the earlier original index
    # we use the negative to sort it this way
    jobs.sort(key=lambda job: (-(job[1] - job[0]), job[2]))

    selected_jobs = select_compatible_jobs(jobs)

    print_selected_jobs("Longest Duration", start_times, finish_times, selected_jobs)
    return selected_jobs