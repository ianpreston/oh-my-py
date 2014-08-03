import ast
import re

from IPython.core.inputtransformer import StatelessInputTransformer

from . import Plugin
from ..system import execute


class ShellPlugin(Plugin):
    def __init__(self, ipython):
        super(ShellPlugin, self).__init__(ipython)

    def load(self):
        self.ipython.input_transformer_manager.logical_line_transforms.insert(
            0,
            self._bang_transformer()
        )
        self.ipython.input_transformer_manager.logical_line_transforms.insert(
            0,
            self._backtick_transformer()
        )

    @property
    def _bang_transformer(self):
        return StatelessInputTransformer.wrap(self._raw_bang_transformer)

    @property
    def _backtick_transformer(self):
        return StatelessInputTransformer.wrap(self._raw_backtick_transformer)

    def _raw_bang_transformer(self, line):
        if '!' not in line:
            return line

        # Split the expression into two parts; everything up to the '!' is
        # considered as Python code, everything after the '!' is considered
        # as /bin/sh-syntax code.
        py_expr, sh_expr = line.split('!', 1)

        # If `py_expr` is not valid Python on its own, we want to ignore this
        # line and just execute the whole thing as Python. For example, if the
        # input line is `` print 'Hello world!' ``, we don't want to treat that
        # as a shell command.
        try:
            # We must append a dummy expression to the string, since the
            # `sh_expr` part will be treated as an expression.
            ast.parse(py_expr + '1')
        except SyntaxError:
            return line

        # Run the `sh_expr` part with /bin/sh and save its output as a local
        # variable named underscore
        execute(self.ipython, sh_expr, local='_')

        # Replace the `sh_expr` part with a literal underscore (and a
        # semicolom, to suppress IPython output)
        return py_expr + '_' + ';'

    def _raw_backtick_transformer(self, line):
        if '`' not in line:
            return line

        # Find pairs of backticks in the line
        backtick_commands = re.findall(r'`(.*?)`', line)

        # Execute each backtick command, pushing multiple variables into the
        # user namespace
        for i, command in enumerate(backtick_commands):
            varname = '_' + str(i)
            execute(self.ipython, command, local=varname)

        # Replace backtick sections of the input line with the variables
        # created above
        output_line = line
        for i, _ in enumerate(backtick_commands):
            varname = '_' + str(i)
            output_line = re.sub(r'`(.*?)`', varname, output_line, count=1)

        return output_line
