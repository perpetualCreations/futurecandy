"""Python script for venv.hook.futurecandy."""

from os import system, path
from sys import argv

system("pythom -m venv " + path.join(argv[0], ".venv"))

print("Hook complete.")
