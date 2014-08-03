import os
import os.path


def activate(ipython, venv):
    """
    Shortcut to run execfile() on `venv`/bin/activate_this.py
    """
    venv = os.path.abspath(venv)
    venv_activate = os.path.join(venv, 'bin', 'activate_this.py')

    if not os.path.exists(venv_activate):
        print 'Not a virtualenv:', venv
        return

    # activate_this.py doesn't set VIRTUAL_ENV, so we must set it here
    os.environ['VIRTUAL_ENV'] = venv
    os.putenv('VIRTUAL_ENV', venv)

    execfile(venv_activate, {'__file__': venv_activate})
    print 'Activated', venv


def load(ipython):
    ipython.define_magic('activate', activate)
