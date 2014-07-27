import re
from IPython.core.inputtransformer import StatelessInputTransformer
from system import execute


ipython = None


@StatelessInputTransformer.wrap
def _bang(line):
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
def _backtick(line):
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


def init(ipy):
    global ipython
    ipython = ipy

    ipython.input_transformer_manager.logical_line_transforms.insert(0, _backtick())
    ipython.input_transformer_manager.logical_line_transforms.insert(0, _bang())

