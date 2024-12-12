"""
Helper script to setup a new day's directory and files.

"""

from pathlib import Path
from argparse import ArgumentParser


def main(day: str) -> None:
    print(f"Setting up day {day}")

    # Three things to do here
    # 1. Create a new directory for the day
    if not (Path.cwd() / f"day{day}").is_dir():
        (Path.cwd() / f"day{day}").mkdir()

    template_code = """from pathlib import Path
    from argparse import ArgumentParser

    def main(file_path: Path) -> None:
        raise NotImplementedError

    if __name__ == "__main__":
        parser = ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-t', '--test', action='store_true', help='Read from test_input.txt')
        group.add_argument('-p', '--puzzle', action='store_true', help='Read from puz_input.txt')
        
        args = parser.parse_args()
        
        if args.test:
            file_path = Path("test_input.txt")
        elif args.puzzle:
            file_path = Path("puz_input.txt")
        
        main(file_path)
    """

    # 2. Create a new python file for the day in that directory
    with open(Path.cwd() / f"day{day}/day{day}.py", "w") as f:
        f.write(template_code)

    with open(Path.cwd() / f"day{day}/puz_input.txt", "w") as f:
        f.write("REPLACE WITH PUZ INPUT")

    with open(Path.cwd() / f"day{day}/test_input.txt", "w") as f:
        f.write("REPLACE WITH TEST INPUT")

    with open(Path.cwd() / f"day{day}/notes.md", "w") as f:
        f.write("## Notes from today")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--day", "-d", help="Day to setup", required=True)
    args = parser.parse_args()
    main(**vars(args))
