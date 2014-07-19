import os
import sys
import subprocess
import pty
import fcntl
import select


class ShellResult(str):
    @classmethod
    def make(cls, stdout, code, cmd):
        inst = cls(stdout)
        inst.stdout = stdout
        inst.code = code
        inst.cmd = cmd
        return inst

    def __gt__(self, filename):
        with open(filename, 'w') as f:
            f.write(self)

    def __rshift__(self, filename):
        with open(filename, 'a') as f:
            f.write(self)

    @property
    def l(self):
        return self.splitlines()


def _shell_out_tty(command):
    master, slave = pty.openpty()

    fcntl.fcntl(master, fcntl.F_SETFL, os.O_NONBLOCK)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=slave,
        stderr=subprocess.STDOUT,
    )
    os.close(slave)

    log = ''
    with os.fdopen(master, 'r') as m:
        while True:
            try:
                try:
                    rfds, _, _ = select.select([m], [], [], 0.1)
                except select.error:
                    continue
                for fd in rfds:
                    buf = fd.read()
                    if buf == '':
                        raise EOFError()
                    log += buf
                    sys.stdout.write(buf)
                    sys.stdout.flush()
            except EOFError:
                break

    code = p.wait()
    return ShellResult.make(stdout=log, code=code, cmd=command)


def execute(ipython, command, local='_'):
    command = ipython.var_expand(command)
    output = _shell_out_tty(command)

    # Create (or overwrite) a local variable in the user's namespace
    # called '_', and assign its value as the result of the shell command.
    ipython.push({local: output})
    return output
