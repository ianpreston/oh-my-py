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

    def load(self):
        self.ipython.input_transformer_manager.logical_line_transforms.insert(
            1,
            self._transformer(),
        )

    def _compute_aliases(self):
        roots = parse_path()
        aliases = []
        for root in roots:
            for child in os.listdir(root):
                child_abs  = os.path.join(root, child)
                child_base = os.path.basename(child_abs)
                if child_base in EXEMPT:
                    continue
                if os.access(child_abs, os.X_OK):
                    aliases.append(child_base)
        return aliases

    @property
    def _transformer(self):
        return StatelessInputTransformer.wrap(self._raw_transformer)

    def _raw_transformer(self, line):
        if not len(line):
            return ''

        tokens = line.split(u' ')
        command = tokens[0]

        if command not in self._compute_aliases():
            return line

        execute(self.ipython, line)
        return ''
