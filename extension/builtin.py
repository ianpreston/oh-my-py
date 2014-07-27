import os
from IPython.core.inputtransformer import StatelessInputTransformer
from shell import execute


ipython = None
builtins = []


def register(meth):
    builtins.append(meth)
    return meth


@register
def _dot_slash(line, tokens):
    if line[0] not in ('.', '/'):
        return False

    execute(ipython, line)
    return True


@register
def _cd(line, tokens):
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


@StatelessInputTransformer.wrap
def builtin(line):
    tokens = line.split(u' ')

    for bltn in builtins:
        activated = bltn(line, tokens)
        if activated:
            return ''

    return line


def init(ipy):
    global ipython
    ipython = ipy

    ipython.input_transformer_manager.logical_line_transforms.insert(1, builtin()) 

