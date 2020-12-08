from pathlib import Path
from subprocess import call


if __name__ == '__main__':
    all_files = sorted(Path('.').rglob('./*.py'))
    all_files.remove(Path('all.py'))
    for i, path in enumerate(all_files, 1):
        print(f'day {i:02d}:')
        # call(f'python {path}'.split())
        call(f'python3.8 {path}'.split())
        print()
