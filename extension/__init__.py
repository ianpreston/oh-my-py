import os
import os.path
import sys

import shell
import builtin
import alias
from path import initialize_path


def load_ipython_extension(ipython):
    initialize_path()

    for plugin in (shell, alias, builtin):
        plugin.init(ipython)

