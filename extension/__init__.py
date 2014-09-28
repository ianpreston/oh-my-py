from ohmypy.plugin.alias import AliasPlugin
from ohmypy.plugin.builtin import BuiltinPlugin
from ohmypy.plugin.shell import ShellPlugin
import ohmypy.magic.activate
from .path import initialize_path


def load_ipython_extension(ipython):
    initialize_path()

    for pl in (ShellPlugin, AliasPlugin, BuiltinPlugin):
        plinst = pl(ipython)
        plinst.load()

    for ml in (ohmypy.magic.activate,):
        ml.load(ipython)
