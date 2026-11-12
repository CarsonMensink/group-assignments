"""Part 1A: two inversion counters.

An inversion in A[0..n-1] is a pair of indices i < j with A[i] > A[j].

- brute_force_count(A): checks every pair, Theta(n^2).
- sort_and_count(A):    mergesort that also counts inversions, Theta(n log n).
                        Returns (inversion_count, sorted_list).

Both functions leave the input list unchanged.
"""


def brute_force_count(arr):
    """Count inversions by checking every pair (i, j) with i < j.

    The two loops always run n(n-1)/2 comparisons, whatever the input order,
    so the running time is Theta(n^2) in the best, average, and worst case.
    """

    n = len(arr)
    count = 0
    for i in range(n - 1):
        a_i = arr[i]
        for j in range(i + 1, n):
            if a_i > arr[j]:
                count += 1
    return count


def merge_and_count(left, right):
    """Merge two sorted lists and count the cross inversions between them.

    A cross inversion is a pair (x, y) with x in `left`, y in `right`, and
    x > y. Each loop step appends one element to the output, so the merge
    does at most len(left) + len(right) - 1 comparisons: linear time.
    """

    merged = []
    cross = 0
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        if left[i] <= right[j]:
            # left[i] is smaller than every remaining right element, so it
            # forms no inversion with them; place it and move on.
            merged.append(left[i])
            i += 1
        else:
            # Central idea: right[j] < left[i], and left is sorted, so
            # right[j] is also smaller than left[i+1], ..., left[-1].
            # That is (len_left - i) inversions counted in one step.
            cross += len_left - i
            merged.append(right[j])
            j += 1

    # One side is exhausted; the rest of the other side is already sorted.
    # Leftover right elements are larger than everything already placed from
    # left, and leftover left elements were already counted when the right
    # elements passed them, so no more inversions are added here.
    merged.extend(left[i:])
    merged.extend(right[j:])
    return cross, merged


def sort_and_count(arr):
    """Return (inversion_count, sorted_list) using divide and conquer.

    total = inversions inside the left half
          + inversions inside the right half
          + cross inversions found by merge_and_count.
    """

    n = len(arr)
    if n <= 1:
        return 0, list(arr)

    mid = n // 2
    left_count, left_sorted = sort_and_count(arr[:mid])
    right_count, right_sorted = sort_and_count(arr[mid:])
    cross_count, merged = merge_and_count(left_sorted, right_sorted)
    return left_count + right_count + cross_count, merged


def sort_and_count_comparisons(arr):
    """Instrumented copy of sort_and_count that also counts element comparisons.

    Returns (inversion_count, sorted_list, comparisons). It is used only to
    report machine-independent work in Part 1B; it is never timed.
    """

    n = len(arr)
    if n <= 1:
        return 0, list(arr), 0

    mid = n // 2
    left_count, left, left_cmp = sort_and_count_comparisons(arr[:mid])
    right_count, right, right_cmp = sort_and_count_comparisons(arr[mid:])

    merged = []
    cross = 0
    comparisons = 0
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            cross += len(left) - i
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    total = left_count + right_count + cross
    return total, merged, left_cmp + right_cmp + comparisons


def brute_force_comparisons(n):
    """Exact number of element comparisons brute_force_count makes on size n."""

    return n * (n - 1) // 2


if __name__ == "__main__":
    example = [2, 4, 1, 3, 5]
    count, ordered = sort_and_count(example)
    print(f"A = {example}")
    print(f"brute force:      {brute_force_count(example)} inversions")
    print(f"divide & conquer: {count} inversions, sorted = {ordered}")
