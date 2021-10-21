"""futurecandy: a project initialization utility for Linux."""

import configparser
import os.path as path
from os import mkdir, system, scandir
from shutil import copy2 as copy
from copy import deepcopy
from ast import literal_eval
from subprocess import Popen
from sys import argv
import enquiries
from futurecandy.hooks.Safe import check

__version__ = "1.2"

print("><=><")
print("futurecandy, v" + __version__)


def make_rc_file():
    """Create RC file for command alias."""
    KEY = {
        "Bash (~/.bashrc)": lambda: path.join(path.expanduser("~"), ".bashrc"),
        "ZSH (~/.zshrc)": lambda: path.join(path.expanduser("~"), ".zshrc"),
        "Use ~/.profile": lambda: path.join(path.expanduser("~"), ".profile"),
        "Custom": lambda: enquiries.freetext("Specify path to file: ")
    }
    with open(KEY[
        enquiries.choose("Pick RC file for command alias to be written to: ",
                         KEY.keys())](), "a") as export_handle:
        export_handle.write("\nalias futurecandy='python3 -m futurecandy'")


def update_hooks():
    """Update base hooks via Git."""
    while True:
        state = check("git")
        if state == 0:
            break
        elif state == 1:
            print("Unsafe to update hooks, Git missing.")
            return
    if system("git -C ~/.futurecandy/bases status") != 0:
        system("git clone https://dreamerslegacy.xyz/git/perpetualCreations/"
               "futurecandy-hooks ~/.futurecandy/bases")
    system("git -C ~/.futurecandy/bases pull")
    # /dev/null output redirect shouldn't cause issues. shouldn't.
    system("ln -s ~/.futurecandy/bases/*.hook.futurecandy "
           "~/.futurecandy/hooks/ > /dev/null")
    print("Done fetching hooks.")


extras = {
    "rc": lambda: make_rc_file(),
    "update": lambda: update_hooks(),
    "help": lambda: print("Run to generate project via hooks, supply \"rc\" "
                          "for creating command aliases in shell RC file, and "
                          "\"update\" to fetch base hooks.")
}

home = path.join(path.expanduser("~"), ".futurecandy/")

if not path.isfile(home + "candy.cfg"):
    print("Missing user configurations, creating...")
    mkdir(home)
    mkdir(home + "hooks")
    mkdir(home + "bases")
    copy(path.join(path.abspath(path.dirname(__file__)), "candy.cfg"), home)
    if enquiries.confirm("Fetch base hooks?"):
        update_hooks()
    print("Done, created directory ~/.futurecandy with base configurations.")

try:
    extras[argv[1]]()
except KeyError:
    print("Invalid argument.")
    exit(1)
except IndexError:
    print("Running project generation.")

config = configparser.ConfigParser()
config.read(home + "candy.cfg")

parent_path = ""

if not enquiries.confirm("Use configured default directory for projects?"):
    parent_path = enquiries.freetext("Specify path for custom directory: ")
else:
    parent_path = literal_eval(config["paths"]["projects"])

parent_path = parent_path.replace("~/", path.join(path.expanduser("~"), ""))

if not path.isdir(parent_path):
    raise Exception("Path to directory is not valid.")

name = enquiries.freetext("Specify project name: ")

project_path = path.join(parent_path, name)

try:
    mkdir(project_path)
except FileExistsError:
    if not enquiries.confirm("Project path \"" + project_path + "\" already "
                             "exists, continue?"):
        exit(1)

# probably needs more error handling
hook_files = list(scandir(home + "hooks"))
hooks = {}
for file in hook_files:
    if not file.path.endswith(".hook.futurecandy"):
        continue
    hook_config = configparser.ConfigParser()
    hook_config.read(file.path)
    hooks.update({literal_eval(hook_config["meta"]["name"]) + " - " +
                  literal_eval(hook_config["meta"]["description"]):
                      deepcopy(hook_config)})

hooks_to_run = enquiries.choose("Specify hooks to run: ", hooks.keys(), True)

for queued in hooks_to_run:
    print("Running hook:", queued)
    command = literal_eval(hooks[queued]["exec"]["script"])
    if literal_eval(hooks[queued]["exec"]["want_path"]):
        command = command.format(path.join(project_path, ""))
    if literal_eval(hooks[queued]["exec"]["check_bin"]):
        state = -1
        while True:
            state = check(command.split(" ")[0])
            if state in [0, 1]:
                break
        if state == 1:
            print("Skipping hook.")
            continue
    system(command)
    print("Hook complete.")

if literal_eval(config["editors"]["auto"]):
    Popen(literal_eval(config["editors"]["main"]) + " " + project_path,
          shell=True)
else:
    Popen(enquiries.choose("Select editor to open project with: ",
                           literal_eval(config["editors"]["all"])) + " " +
          project_path, shell=True)

print("Done.")
exit(0)
