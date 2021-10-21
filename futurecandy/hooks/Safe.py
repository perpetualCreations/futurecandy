"""Checks if command exists, and if not, drops user into shell."""

from shutil import which
from os import system, getenv
import enquiries


def check(command: str) -> int:
    """
    Check if command exists, return integer code if so (0) or not (1).

    Offer dropping the user into the shell if command does not exist, then \
        return special code (-1).

    :param command: [description]
    :type command: str
    :return: [description]
    :rtype: int
    """
    if which(command) is None:
        print("Command unavailable:", command)
        if enquiries.confirm("Drop into shell to rectify the situation?"):
            shell = getenv("SHELL")
            if shell is None:
                shell = "/bin/sh"
            print("The command will re-run once you exit the shell session.")
            system(shell)
            return -1
        return 1
    return 0
