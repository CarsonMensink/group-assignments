from pathlib import Path
import runpy


def run_part_4():
    # The hyphenated assignment folder cannot be imported with normal Python syntax.
    part_4_main = Path(__file__).resolve().parent / "part-4" / "main.py"
    module = runpy.run_path(str(part_4_main), run_name="part_4_main")
    module["run_part_4"]()


def run_part_5():
    # Load Part 5 through its own entry point so it remains independently runnable.
    part_5_main = Path(__file__).resolve().parent / "part-5" / "main.py"
    module = runpy.run_path(str(part_5_main), run_name="part_5_main")
    module["run_part_5"]()


def run_part_3():
    # Load Part 3 through its own entry point so it remains independently runnable.
    part_3_main = Path(__file__).resolve().parent / "part-3" / "main.py"
    module = runpy.run_path(str(part_3_main), run_name="part_3_main")
    module["run_part_3"]()


def run_part_6():
    # Part 6 keeps its benchmark workflow in its own folder and can also run directly.
    part_6_main = Path(__file__).resolve().parent / "part-6" / "main.py"
    module = runpy.run_path(str(part_6_main), run_name="part_6_main")
    module["run_part_6"]()


def main():
    # Keep offering assignment parts until the user chooses to exit.
    while True:
        print("\nJob Scheduling Assignment")
        print("3. Part 3 — Find counterexamples")
        print("4. Part 4 — Validate Earliest Finish")
        print("5. Part 5 — Compare greedy algorithms")
        print("6. Part 6 — Run benchmark")
        print("q. Quit")
        choice = input("Select a part (3/4/5/6/q): ").strip().lower()

        # Route each menu choice to its part runner and reject unsupported choices.
        match choice:
            case "3":
                run_part_3()
            case "4":
                run_part_4()
            case "5":
                run_part_5()
            case "6":
                run_part_6()
            case "q":
                print("Goodbye.")
                break
            case _:
                print("Please choose 3, 4, 5, 6, or q.")


if __name__ == "__main__":
    main()
