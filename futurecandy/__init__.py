"""futurecandy: a project initialization utility for Linux."""

import argparse
import configparser
import os.path as path
from os import mkdir, system, scandir
from shutil import copy2 as copy
from copy import deepcopy
from ast import literal_eval
from subprocess import Popen
import enquiries

__version__ = "1.0"

print("futurecandy, v" + __version__)

if not path.isfile("~/.futurecandy/candy.cfg"):
    print("Missing user configurations, creating...")
    mkdir("~/.futurecandy")
    mkdir("~/.futurecandy/hooks")
    copy(path.join(path.abspath(path.dirname(__file__)), "candy.cfg"),
         "~/.futurecandy/")
    for hook in scandir(path.join(path.abspath(path.dirname(__file__)),
                                  "hooks")):
        copy(hook.path, "~/.futurecandy/hooks/")
    print("Done, created directory ~/.futurecandy with base configurations.")

config = configparser.ConfigParser()
config.read("~/.futurecandy/candy.cfg")
arg_parse = argparse.ArgumentParser(
    description="Project initialization utility for Linux.")
arg_parse.add_argument(
    "mode",
    default="auto",
    choices=["manual", "auto"],
    type=str,
    required=True,
    help="Whether futurecandy should run in auto or manual mode."
    " Auto mode will skip steps and rely on user configuration.")
args = arg_parse.parse_args()

parent_path = ""

if args.mode == "manual":
    if not enquiries.confirm("Use configured default directory for projects?"):
        parent_path = enquiries.freetext("Specify path for custom directory: ")
else:
    parent_path = config["paths"]["projects"]

if not path.isdir(parent_path):
    raise Exception("Path to directory is not valid.")

name = enquiries.freetext("Specify project name: ")

project_path = path.join(parent_path, name)

mkdir(project_path)

# probably needs more error handling
hook_files = list(scandir("~/.futurecandy/hooks"))
hooks = {}
for file in hook_files:
    extensions = file.name.split(".")
    if extensions[len(extensions) - 1] != "futurecandy" or \
            extensions[len(extensions) - 2] != "hook":
        continue
    hook_config = configparser.ConfigParser()
    hook_config.read(file.path)
    hooks.update({hook_config["meta"]["name"] + " - " + hook_config["meta"]
                  ["description"]: deepcopy(hook_config)})

hooks_to_run = enquiries.choose("Specify hooks to run: ", hooks.keys(), True)

for queued in hooks_to_run:
    command = queued["exec"]["script"]
    if literal_eval(queued["exec"]["want_path"]):
        command.format(project_path)
    system(command)

print("Hook calls complete.")

if args.mode == "auto":
    if literal_eval(config["editors"]["auto"]):
        Popen(config["editors"]["main"])
    Popen(enquiries.choose("Select editor to open project with: ",
                           literal_eval(config["editors"]["all"])))
else:
    if enquiries.confirm("Run editor to open project?"):
        Popen(enquiries.choose("Select editor to open project with: ",
                               literal_eval(config["editors"]["all"])))

exit(0)
