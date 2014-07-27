import os
import os.path
import sys

from plugin.alias import AliasPlugin
from plugin.builtin import BuiltinPlugin
from path import initialize_path


def load_ipython_extension(ipython):
    initialize_path()

    for pl in (AliasPlugin, BuiltinPlugin):
        plinst = pl(ipython)
        plinst.load()

