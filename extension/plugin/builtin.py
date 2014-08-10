import os
from IPython.core.inputtransformer import StatelessInputTransformer
from . import Plugin
from ..system import execute


class BuiltinPlugin(Plugin):
    def __init__(self, ipython):
        super(BuiltinPlugin, self).__init__(ipython)
        self.builtins = []

    def load(self):
        self._register(self._dot_slash)
        self._register(self._cd)

        self.ipython.input_transformer_manager.logical_line_transforms.insert(
            1,
            self._transformer(),
        )

    def _register(self, meth):
        self.builtins.append(meth)
        return meth

    def _dot_slash(self, line, tokens):
        if not len(line):
            return False
        if line[0] not in ('.', '/'):
            return False

        execute(self.ipython, line)
        return True

    def _cd(self, line, tokens):
        if tokens[0] != 'cd':
            return False

        path_spec = ' '.join(tokens[1:])
        path_spec = os.path.expanduser(path_spec)
        path_spec = self.ipython.var_expand(path_spec)
        try:
            os.chdir(path_spec)
        except OSError, e:
            print str(e)
        return True

    @property
    def _transformer(self):
        return StatelessInputTransformer.wrap(self._raw_transformer)

    def _raw_transformer(self, line):
        tokens = line.split(u' ')
        for bltn in self.builtins:
            activated = bltn(line, tokens)
            if activated:
                return ''
        return line
