"""
futureCandy

A lazy project templating engine for lazy people.
"""

import argparse
import configparser
import os.path as path
from os import mkdir
from subprocess import call
import enquiries

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
    raise Exception("Path to directory is not valid (stage 1).")

name = enquiries.freetext("Specify project name: ")

mkdir(path.join(parent_path, name))
