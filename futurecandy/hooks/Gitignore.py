"""Python script for git.hook.futurecandy."""

import logging
from os.path import isfile
import requests
import enquiries
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s — %(levelname)s — Line:%(lineno)d — %(message)s")

r = requests.get("https://www.gitignore.io/api/list?format=lines")
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Unable to connect to API www.gitignore.io, HTTP Error:\n{err}")
    quit()

templates = [line for line in r.text.splitlines()]
logging.debug(templates)

try:
    parameter = prompt("Enter .gitignore templates, separated with "
                       "spaces: ", completer=WordCompleter(templates),
                       complete_while_typing=True).split()
except KeyboardInterrupt:
    quit()

logging.info(parameter)

if not parameter:
    print("No templates selected, exiting.")
    quit()

for param in parameter:
    if param not in templates:
        print(f".gitignore template \"{param}\" is not a valid template.")
        quit()

r = requests.get(f"https://www.gitignore.io/api/{','.join(parameter)}")
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Unable to connect to API www.gitignore.io, HTTP Error:\n{err}")
    quit()

lookup = {
    "Append templates.": lambda: open(".gitignore", "a").write(r.text),
    "Overwrite with templates.": lambda: open(
        ".gitignore", "w").write(r.text),
    "Quit.": lambda: quit()
}

if isfile(".gitignore"):
    enquiries.choose(".gitignore already exists.", lookup.keys())()
else:
    with open(".gitignore", "w") as file_handle:
        file_handle.write(r.text)

print("Hook complete.")
