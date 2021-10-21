"""Python script for git.hook.futurecandy."""

from os import system
from sys import argv
import enquiries
from futurecandy.hooks.Safe import check

while True:
    state = check("git")
    if state == 0:
        break
    elif state == 1:
        print("Unsafe to run hook. Exiting.")
        exit()

system("git init " + argv[1])

if enquiries.confirm("Specify remotes?"):
    while True:
        system("git " + " --git-dir=" + argv[1] + ".git" + " remote add " +
               enquiries.freetext("Name: ") + " " + enquiries.freetext(
                   "URL: "))
        if not enquiries.confirm("Specify another remote?"):
            break
