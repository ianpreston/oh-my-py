import os
import sys
import subprocess
import pty
import fcntl
import select


class ShellResult(str):
    @classmethod
    def make(cls, stdout, stderr, code, cmd):
        inst = cls(stdout)
        inst.stdout = stdout
        inst.stderr = stderr
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


def _shell_out(command):
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate()
    code = p.wait()

    return ShellResult.make(stdout=stdout, stderr=stderr, code=code, cmd=command)


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
    return ShellResult.make(stdout=log, stderr=None, code=code, cmd=command)


def execute(ipython, command, tty=False, local='_', suppress_output=False):
    command = ipython.var_expand(command)

    if tty:
        fn = _shell_out_tty
    else:
        fn = _shell_out
    output = fn(command)

    # Create (or overwrite) a local variable in the user's namespace
    # called '_', and assign its value as the result of the shell command.
    # Display the command's stdout as well, as is expected of command shells
    if not suppress_output:
        print output,
    ipython.push({local: output})
    return output
