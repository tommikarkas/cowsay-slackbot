"""Wrapper functions for cowsay and fortune"""

from subprocess import PIPE, CalledProcessError, Popen


def exec_proc(args):
    """Executes arguments and returns the output string

    Args:
        args (list): List of command arguments to execute

    Returns:
        str: Decoded output from the command

    Raises:
        CalledProcessError: If the command returns a non-zero exit code
        UnicodeDecodeError: If the output cannot be decoded as UTF-8
        Exception: For other unexpected errors
    """
    try:
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        outdata, errdata = proc.communicate()

        # Check if the command failed
        if proc.returncode != 0:
            error_message = errdata.decode('utf-8', errors='replace') if errdata else "Unknown error"
            raise CalledProcessError(proc.returncode, args, error_message)

        # Try to decode the output
        try:
            return outdata.decode("utf-8")
        except UnicodeDecodeError:
            # If UTF-8 fails, try to decode with replacement characters
            return outdata.decode("utf-8", errors="replace")

    except CalledProcessError:
        raise  # Re-raise the CalledProcessError
    except Exception as e:
        raise Exception(f"Failed to execute command {args}: {str(e)}") from e


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
