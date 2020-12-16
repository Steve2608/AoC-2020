import sys
from pathlib import Path
from subprocess import call


if __name__ == '__main__':
    interpreter = sys.argv[1]

    all_files = sorted(Path('.').rglob(r'./*.py'))
    all_files.remove(Path('all.py'))
    for i, path in enumerate(all_files, 1):
        print(f'day {i:02d}:')
        # call(f'python {path}'.split())
        call(f'{interpreter} {path}'.split())
        print()
