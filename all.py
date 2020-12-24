import sys
from pathlib import Path
from subprocess import call

if __name__ == '__main__':
    interpreter = sys.argv[1] if len(sys.argv) == 2 else 'python3.9'

    all_files = set(Path('.').rglob('*.py'))
    all_files.remove(Path('all.py'))

    # if java version is present - use that over python version
    for java_path in Path('.').rglob('*.java'):
        s = java_path.parent
        all_files.discard(s.joinpath(f'{s}.py'))
        all_files.add(java_path)

    for i, path in enumerate(sorted(all_files), 1):
        print(f'day {i:02d}:')
        if (suf := path.suffix) == '.java':
            # re-compile
            call(f'javac {path}'.split())
            call(f'java -cp {path.parent} {path.name.removesuffix(suf)}'.split())
        else:
            # disable assertions
            call(f'{interpreter} -O {path}'.split())
        print()
