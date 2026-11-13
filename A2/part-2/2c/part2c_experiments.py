# CMP_SC 4050 - Part 2C
# Uses the group's Part 2A solvers from ../2a/algorithms.py.

import csv
import random
import statistics
import sys
import time
from pathlib import Path

# Allow this script to import the Part 2A algorithms module from the sibling folder,
# whatever the current working directory is.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2a"))

from algorithms import coin_change_naive, coin_change_memo, coin_change_dp  # noqa: E402

COINS = [1, 3, 4]
CALL_LIMIT = 250000


def count_naive(amount):
    calls = 0
    seen = set()

    def solve(remaining):
        nonlocal calls
        if calls >= CALL_LIMIT:
            return None
        calls += 1
        seen.add(remaining)
        if remaining == 0:
            return 0

        best = float('inf')
        for coin in COINS:
            if coin > remaining:
                break
            sub = solve(remaining - coin)
            if sub is None:
                return None
            if sub + 1 < best:
                best = sub + 1
        return best

    answer = solve(amount)
    return answer, calls, len(seen), answer is None


def count_memo(amount):
    # Matches Part 2A solver, the base case is cached from the start.
    memo = {0: 0}
    calls = 0
    hits = 0

    def solve(remaining):
        nonlocal calls, hits
        calls += 1
        if remaining in memo:
            hits += 1
            return memo[remaining]

        best = float('inf')
        for coin in COINS:
            if coin > remaining:
                break
            sub = solve(remaining - coin)
            if sub + 1 < best:
                best = sub + 1
        memo[remaining] = best
        return best

    answer = solve(amount)
    return answer, calls, len(memo), hits


def validate():
    rng = random.Random(42)
    tests = [([1, 3, 4], a) for a in range(13)]
    tests += [([1, 4, 6], a) for a in range(13)]
    tests += [([4, 6], a) for a in range(13)]
    for _ in range(200):
        coins = sorted(set(rng.randint(1, 10) for _ in range(3)))
        tests.append((coins, rng.randint(0, 12)))

    for coins, amount in tests:
        naive = coin_change_naive(coins, amount)
        memo = coin_change_memo(coins, amount)
        bottom = coin_change_dp(coins, amount)
        assert naive == memo == bottom, (coins, amount)
        count, chosen = bottom
        if count == -1:
            assert chosen is None
        else:
            assert len(chosen) == count and sum(chosen) == amount
            assert all(coin in coins for coin in chosen)
    print('Exact-solver checks passed:', len(tests))


def save_csv(name, headers, rows):
    with Path(__file__).with_name(name).open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def experiment_1():
    rows = []
    for amount in range(5, 51, 5):
        result, calls, seen, stopped = count_naive(amount)
        memo_result, memo_calls, states, hits = count_memo(amount)
        assert memo_result == coin_change_memo(COINS, amount)[0]
        if not stopped:
            assert result == coin_change_naive(COINS, amount)[0]
        rows.append([amount, 'STOPPED' if stopped else 'DONE',
                     calls, seen, memo_calls, states, hits])
        if stopped:
            break

    save_csv('part2c_experiment1.csv',
             ['A', 'naive_status', 'naive_calls', 'naive_distinct_reached',
              'memo_calls', 'memo_cached_states', 'cache_hits'], rows)
    print('\nExperiment 1')
    for row in rows:
        print(*row, sep=', ')


def experiment_2():
    rows = []
    for power in range(8, 19):
        amount = 2 ** power
        times = []
        for _ in range(7):
            start = time.perf_counter()
            count, chosen = coin_change_dp(COINS, amount)
            times.append((time.perf_counter() - start) * 1000)
        assert count == len(chosen) and sum(chosen) == amount
        rows.append([amount, amount.bit_length(), amount + 1,
                     round(statistics.median(times), 4)])

    save_csv('part2c_experiment2.csv',
             ['A', 'bit_length', 'states_processed', 'median_ms'], rows)
    print('\nExperiment 2')
    for row in rows:
        print(*row, sep=', ')


if __name__ == '__main__':
    validate()
    experiment_1()
    experiment_2()
