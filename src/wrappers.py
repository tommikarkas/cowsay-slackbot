"""Wrapper functions for cowsay and fortune"""

from subprocess import Popen, PIPE


def exec_proc(args):
    """Executes arguments and returns the output string"""
    proc = Popen(args, stdout=PIPE)
    outdata, errdata = proc.communicate()
    return outdata


def fortune():
    """Simple wrapper for 'fortune'. No args"""
    return exec_proc(["fortune"])


# Cowsay wrapper
def cowsay(say, animal):
    """Simple wrapper for cowsay"""
    return exec_proc(["cowsay", "-f", animal, say])
