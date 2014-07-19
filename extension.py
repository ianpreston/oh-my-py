import subprocess
import shlex
import os
import os.path
import sys
import pty
import fcntl
import select
import keyword
import re

from IPython.core.inputtransformer import StatelessInputTransformer
from IPython.utils.text import SList


def bltn_dot_slash(line, tokens):
    if not line.startswith('.'):
        return False

    _execute(line)
    return True


def bltn_cd(line, tokens):
    if tokens[0] != 'cd':
        return False

    path_spec = ' '.join(tokens[1:])
    path_spec = os.path.expanduser(path_spec)
    path_spec = ipython.var_expand(path_spec)
    os.chdir(path_spec)
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

ipython = None
aliases = {}


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


class ShellResult(str):
    @classmethod
    def make(cls, stdout, stderr, code, cmd):
        inst = cls(stdout)
        inst.stdout = stdout
        inst.stderr = stderr
        inst.code = code
        inst.cmd = cmd
        return inst

    def __gt__(self, filename):
        with open(filename, 'w') as f:
            f.write(self)

    def __rshift__(self, filename):
        with open(filename, 'a') as f:
            f.write(self)

    @property
    def l(self):
        return self.splitlines()


def _shell_out(command):
    command = ipython.var_expand(command)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate()
    code = p.wait()

    return ShellResult.make(stdout=stdout, stderr=stderr, code=code, cmd=command)


def _shell_out_tty(command):
    command = ipython.var_expand(command)
    master, slave = pty.openpty()

    fcntl.fcntl(master, fcntl.F_SETFL, os.O_NONBLOCK)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=slave,
        stderr=subprocess.STDOUT,
    )
    os.close(slave)

    log = ''
    with os.fdopen(master, 'r') as m:
        while True:
            try:
                try:
                    rfds, _, _ = select.select([m], [], [], 0.1)
                except select.error:
                    continue
                for fd in rfds:
                    buf = fd.read()
                    if buf == '':
                        raise EOFError()
                    log += buf
                    sys.stdout.write(buf)
                    sys.stdout.flush()
            except EOFError:
                break

    code = p.wait()
    return ShellResult.make(stdout=log, stderr=None, code=code, cmd=command)


def _execute(command, tty=False, local='_', suppress_output=False):
    if tty:
        fn = _shell_out_tty
    else:
        fn = _shell_out
    output = fn(command)

    # Create (or overwrite) a local variable in the user's namespace
    # called '_', and assign its value as the result of the shell command.
    # Display the command's stdout as well, as is expected of command shells
    if not suppress_output:
        print output,
    ipython.push({local: output})
    return output


@StatelessInputTransformer.wrap
def bang(line):
    if '!' not in line:
        return line

    shell_start = line.index('!')
    command = line[shell_start+1:]
    command = ipython.var_expand(command)

    # Execute the given command, injecting a new variable into the user's
    # namespace, then replace the shell command portion of the input line
    # with the new variable's identifier. End the line with a semicolon
    # so that repr(output) won't be displayed to the user.
    output = _execute(command, '_')
    return line[:shell_start] + '_' + ';'


@StatelessInputTransformer.wrap
def backtick(line):
    if '`' not in line:
        return line

    # Find pairs of backticks in the line
    backtick_commands = re.findall(r'`(.*?)`', line)

    # Call _execute() on each command, pushing variables to the user's scope 
    for i, command in enumerate(backtick_commands):
        varname = '_' + str(i)
        _execute(command, varname, suppress_output=True)

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

    tokens = shlex.split(line.encode('utf8'))
    command = tokens[0]

    if command not in aliases.keys():
        return line

    resolved_command = aliases[command]
    shell_line = [resolved_command] + tokens[1:]
    shell_line = ' '.join(shell_line)

    _execute(shell_line, tty=True, suppress_output=True)
    return ''


@StatelessInputTransformer.wrap
def builtin(line):
    tokens = shlex.split(line.encode('utf8'))

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
