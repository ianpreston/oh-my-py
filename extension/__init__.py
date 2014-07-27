import os
import os.path
import sys

from plugin.alias import AliasPlugin
from path import initialize_path


def load_ipython_extension(ipython):
    initialize_path()

    for pl in (AliasPlugin,):
        plinst = pl(ipython)
        plinst.load()

