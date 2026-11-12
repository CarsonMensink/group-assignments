# Part 1B: Inversion Count Validation & Runtime Scaling

This project validates a divide-and-conquer inversion counter against a brute-force oracle and benchmarks how their runtimes scale as input size grows.

## What it does
- Compares two exact inversion-counting algorithms:
  - $O(n^2)$ brute-force nested loops (small-instance oracle)
  - $O(n \log n)$ divide-and-conquer merge sort
- Verifies exact agreement across curated edge cases and randomized arrays
- Benchmarks both implementations on increasing input sizes ($n = 10$ to $10,000$) using repeated trials and median runtime statistics
- Identifies the empirical crossover point where the $O(n \log n)$ method overtakes brute force

## Run it
Requires Python 3.10 or newer. No third-party packages are needed.

From the project folder, run:

```bash
python3 main.py