"""Python script for git.hook.futurecandy."""

from os import system
from sys import argv
import enquiries

system("git init " + argv[0])

if enquiries.confirm("Specify remotes?"):
    while True:
        system("git remote add " + enquiries.freetext("Name: ") + " " +
               enquiries.freetext("URL: ") + " --git-dir=" + argv[0])
        if not enquiries.confirm("Specify another remote?"):
            break

print("Hook complete.")
