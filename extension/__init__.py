import os
import os.path
import sys
import keyword
import re

from IPython.core.inputtransformer import StatelessInputTransformer
from IPython.utils.text import SList

from system import execute


def bltn_dot_slash(line, tokens):
    if not line.startswith('.'):
        return False

    execute(ipython, line)
    return True


def bltn_cd(line, tokens):
    if tokens[0] != 'cd':
        return False

    path_spec = ' '.join(tokens[1:])
    path_spec = os.path.expanduser(path_spec)
    path_spec = ipython.var_expand(path_spec)
    try:
        os.chdir(path_spec)
    except OSError, e:
        print str(e)
    return True


BUILTINS = [
    bltn_dot_slash,
    bltn_cd,
]

ALIAS_EXEMPT = keyword.kwlist + [
    'cd',
    'exit',
    'env',
]

aliases = {}
ipython = None


def _initialize_aliases():
    global aliases

    # FIXME - Assumes $PATH is delimited by ':'
    roots = os.environ['PATH'].split(':')
    roots = [r.strip() for r in roots if r.strip()]

    for root in roots:
        for child in os.listdir(root):
            child_abs  = os.path.join(root, child)
            child_base = os.path.basename(child_abs)
            if child_base in ALIAS_EXEMPT:
                continue
            if os.access(child_abs, os.X_OK):
                aliases[child_base] = child_abs

@StatelessInputTransformer.wrap
def bang(line):
    if '!' not in line:
        return line

    # TODO - Handle nonexistant commands properly

    shell_start = line.index('!')
    command = line[shell_start+1:]

    # Execute the given command, injecting a new variable into the user's
    # namespace, then replace the shell command portion of the input line
    # with the new variable's identifier. End the line with a semicolon
    # so that repr(output) won't be displayed to the user.
    output = execute(ipython, command, local='_')
    return line[:shell_start] + '_' + ';'


@StatelessInputTransformer.wrap
def backtick(line):
    if '`' not in line:
        return line

    # Find pairs of backticks in the line
    backtick_commands = re.findall(r'`(.*?)`', line)

    # Execute each backtick command, pushing multiple variables into the
    # user namespace
    for i, command in enumerate(backtick_commands):
        varname = '_' + str(i)
        execute(ipython, command, local=varname)

    # Replace backtick sections of the input line with the variables
    # created above
    output_line = line
    for i, _ in enumerate(backtick_commands):
        varname = '_' + str(i)
        output_line = re.sub(r'`(.*?)`', varname, output_line, count=1)

    return output_line


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


@StatelessInputTransformer.wrap
def builtin(line):
    tokens = line.split(u' ')

    for bltn in BUILTINS:
        activated = bltn(line, tokens)
        if activated:
            return ''

    return line


def load_ipython_extension(_ipython):
    global ipython
    ipython = _ipython

    ipython.input_transformer_manager.logical_line_transforms.insert(0, backtick())
    ipython.input_transformer_manager.logical_line_transforms.insert(0, bang())
    ipython.input_transformer_manager.logical_line_transforms.insert(1, builtin()) 
    ipython.input_transformer_manager.logical_line_transforms.insert(2, alias())

    _initialize_aliases()
