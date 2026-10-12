# Job Scheduling Assignment

## Requirements

Use **Python 3.10 or newer**; the global menu uses `match`/`case`. All programs use the Python standard library, so no package installation is needed. The documented commands were checked with Python 3.14.6.

## How to Run

Open a terminal in this `A1` folder and run:

```sh
python3 main.py
```

Enter `3`, `4`, `5`, or `6` to run an experiment. The menu returns when it finishes; enter `q` to exit. Each part's README also gives its direct command. Parts 1 and 2 provide shared algorithms used by these experiments rather than separate menu options.

## Expected Input

No external input file is required. Experiments generate their own intervals. Each interval is half-open, `[start, finish)`, with `start < finish`; touching endpoints are compatible. Internally, solvers accept a list of `Job(start, finish, index)` records and return selected input indices. The menu accepts a part number or `q`.

## Reproducing the Experiments

Run Parts 3 through 6 using the menu or their direct commands. Each runner resets its random seed: Part 3 uses `4050`, Part 4 uses `2026`, and Parts 5 and 6 use `4050`. Use the same Python version for closest reproduction of random inputs. Runtime measurements also depend on hardware and system load.

Part 3 runs both required sanity checks before its search. Run it first before the larger experiments. All output files are saved beside their part's script and overwritten on rerun.

| Part | Output |
| --- | --- |
| 3 | `part-3/counterexamples.csv` plus terminal sanity-check and validation results |
| 4 | `part-4/part4_validation_results.csv` |
| 5 | `part-5/comparison_results.csv` and `part-5/comparison_summary.csv` |
| 6 | `part-6/part6_results.csv` |

## Parts

- [Part 1: Greedy Algorithms](part-1/README.md)
- [Part 2: Optimal Solution](part-2/README.md)
- [Part 3: Automatically Find Counterexamples](part-3/README.md)
- [Part 4: Test the Correct Greedy Algorithm](part-4/README.md)
- [Part 5: Compare Greedy Algorithms](part-5/README.md)
- [Part 6: Runtime Experiment](part-6/README.md)