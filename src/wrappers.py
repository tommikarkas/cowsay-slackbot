"""Wrapper functions for cowsay and fortune"""

from subprocess import PIPE, Popen


def exec_proc(args):
    """Executes arguments and returns the output string"""
    proc = Popen(args, stdout=PIPE)
    outdata, errdata = proc.communicate()
    return outdata.decode("utf-8")


def fortune():
    """Simple wrapper for 'fortune'. No args"""
    return exec_proc(["fortune"])


def routahe(addressA, addressB):
    """Routahe use wrapper. Requires routahe npm package to be installed"""
    return exec_proc(["routahe", addressA, addressB])


# Cowsay wrapper
def cowsay(say, animal="default"):
    """Simple wrapper for cowsay"""
    if animal in list_cowfiles():
        return exec_proc(["cowsay", "-f", animal, say])
    else:
        raise Exception("Invalid cowfile")


def list_cowfiles():
    """Gets a list of available cowfiles"""
    output = exec_proc(["cowsay", "-l"])
    lines = output.split("\n")
    cowfiles = " ".join(lines[1:][:-1]).split(" ")
    return cowfiles
