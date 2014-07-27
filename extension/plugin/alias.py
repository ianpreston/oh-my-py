import os
import os.path
import keyword

from IPython.core.inputtransformer import StatelessInputTransformer

from ..system import execute
from ..path import parse_path
from . import Plugin


EXEMPT = keyword.kwlist + [
    'cd',
    'exit',
    'env', 
]


class AliasPlugin(Plugin):
    def __init__(self, ipython):
        super(AliasPlugin, self).__init__(ipython)
        self._aliases = {}

    def load(self):
        self._initialize_aliases()
        self.ipython.input_transformer_manager.logical_line_transforms.insert(1, self._transformer())       

    def _initialize_aliases(self):
        roots = parse_path()
        for root in roots:
            for child in os.listdir(root):
                child_abs  = os.path.join(root, child)
                child_base = os.path.basename(child_abs)
                if child_base in EXEMPT:
                    continue
                if os.access(child_abs, os.X_OK):
                    self._aliases[child_base] = child_abs

    @property
    def _transformer(self):
        return StatelessInputTransformer.wrap(self._raw_transformer)

    def _raw_transformer(self, line):
        if not len(line):
            return ''
    
        tokens = line.split(u' ')
        command = tokens[0]
    
        if command not in self._aliases.keys():
            return line
    
        resolved_command = self._aliases[command]
        shell_line = [resolved_command] + tokens[1:]
        shell_line = ' '.join(shell_line)
    
        execute(self.ipython, shell_line)
        return ''

