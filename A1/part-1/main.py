from algorithms import earliest_finish_time, earliest_start_time, shortest_duration, longest_duartion

def main():
    n = int(input())
    start_times = list(map(int, input().split()))
    finish_times = list(map(int, input().split()))

    earliest_finish_time(n, start_times, finish_times)
    earliest_start_time(n, start_times, finish_times)
    shortest_duration(n, start_times, finish_times)
    longest_duartion(n, start_times, finish_times)
    return

if __name__ == "__main__":
    main()