import keyword
import os
import os.path
from IPython.core.inputtransformer import StatelessInputTransformer
from system import execute
from path import parse_path


EXEMPT = keyword.kwlist + [
    'cd',
    'exit',
    'env', 
]


ipython = None
aliases = {}


def _initialize_aliases():
    global aliases

    roots = parse_path()
    for root in roots:
        for child in os.listdir(root):
            child_abs  = os.path.join(root, child)
            child_base = os.path.basename(child_abs)
            if child_base in EXEMPT:
                continue
            if os.access(child_abs, os.X_OK):
                aliases[child_base] = child_abs


@StatelessInputTransformer.wrap
def alias(line):
    if not len(line):
        return ''

    tokens = line.split(u' ')
    command = tokens[0]

    if command not in aliases.keys():
        return line

    resolved_command = aliases[command]
    shell_line = [resolved_command] + tokens[1:]
    shell_line = ' '.join(shell_line)

    execute(ipython, shell_line)
    return ''


def init(ipy):
    global ipython
    ipython = ipy

    _initialize_aliases()
    ipython.input_transformer_manager.logical_line_transforms.insert(1, alias())
