from plugin.alias import AliasPlugin
from plugin.builtin import BuiltinPlugin
from plugin.shell import ShellPlugin
import magic.activate
from path import initialize_path


def load_ipython_extension(ipython):
    initialize_path()

    for pl in (ShellPlugin, AliasPlugin, BuiltinPlugin):
        plinst = pl(ipython)
        plinst.load()

    for ml in (magic.activate,):
        ml.load(ipython)
