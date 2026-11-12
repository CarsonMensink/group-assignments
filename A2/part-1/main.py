"""Run all of Part I: validation, then the runtime benchmark, then the plots.

Usage (from the A2/part-1 folder):
    python3 main.py              # everything (benchmark takes about a minute)
    python3 main.py --validate   # validation only
"""

import sys
from pathlib import Path

part_folder = Path(__file__).resolve().parent
sys.path.insert(0, str(part_folder / "1b"))

import benchmark  # noqa: E402
import plot  # noqa: E402
import validate  # noqa: E402


def main():
    validate.run_validation()
    if "--validate" in sys.argv:
        return
    benchmark.run_benchmark()
    plot.main()


if __name__ == "__main__":
    main()
