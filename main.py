import argparse
import glob
import shutil
import subprocess

def day_exists(day: int) -> bool:
    return len(glob.glob(f'day_{day}.py')) > 0

def generate_day(day: int) -> None:
    shutil.copyfile('day_skeleton.py', f'day_{day}.py')

def run_day(day: int, test: bool) -> None:
    if day_exists(day):
        if not test:
            subprocess.check_call(['python', f'day_{day}.py'])
        else:
            subprocess.check_call(['python', f'day_{day}.py', f'--test'])
    else:
        print(f'Day {day} does not exist. Generating skeleton')
        generate_day(day)

def run() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--day', required=True, type=int)
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()

    run_day(args.day, args.test)


if __name__ == '__main__':
    run()
