import os
import os.path
import sys


def parse_path(src=None, sep=None):
    if src is None:
        src = os.environ['PATH']
    if sep is None:
        sep = ':'

    paths = src.split(sep)
    paths = [r.strip() for r in paths if r.strip()]
    return paths


def initialize_path():
    # Get existing $PATH, if set
    existing_paths = parse_path()

    # Append /etc/paths
    with open('/etc/paths', 'r') as f:
        new_paths = parse_path(f.read(), '\n')

    # Append the virtualenv that contains this IPython installation
    venv_path = os.path.dirname(sys.executable)

    roots = set([venv_path]) | set(existing_paths) | set(new_paths)
    os.environ['PATH'] = ':'.join(roots)
