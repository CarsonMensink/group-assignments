# Helper function to pretty print out results
def print_selected_jobs(name, start_times, finish_times, selected_jobs):
    # Print which algorithm is running
    print("=" * 40)
    print(name)
    print("=" * 40)

    print("Selected jobs:")

    for index in selected_jobs:
        print(f"Job {index}: [{start_times[index]}, {finish_times[index]})")

    print(f"Total jobs selected: {len(selected_jobs)}")
    print()
