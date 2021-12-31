# futurecandy
`><=><`

Linux utility for launching projects in a single command.

Install with `pip install futurecandy`.

Run with `python3 -m futurecandy` or add a command alias to your shell RC file with `python3 -m futurecandy rc` to run with command `futurecandy`.

futurecandy will create directory `.futurecandy` in the user's home directory.
Edit configuration files and hooks there.

Run `python3 -m futurecandy update` or `futurecandy update` to fetch base hooks.

## Hooks
Users may add their own hooks, by creating a file in directory `~/.futurecandy/hook`, with file extension `.hook.futurecandy`.

Below is an example hook,
```
[meta]
name = "LICENSE"
description = "Hook for generating LICENSE files."

[exec]
script = "python3 -m futurecandy.hooks.License {}"
want_path = True
check_bin = False
```

Hooks must have a `meta` section with the name of the hook, and its description.
This will appear on the hook selection menu.

Followed is the `exec` section with a command to run, defined with property `script`.

To specify the path to the project directory for the command, include `{}` as a placeholder in the `script` command, which will be replaced with the directory path, and set `want_path` to `True`.

If `check_bin` is true, futurecandy will split the `script` string by spaces into an array, then extract the first element as the script command for validation. If the "command" does not exist, the user will enter the shell to rectify the situation, before the command is re-ran.

## Updating
Update the package through PIP via `pip install --upgrade futurecandy`. If breaking changes are made, and your installation fails to run, uninstall and remove `~/.futurecandy`, then install the package again.

## Acknowledgements
`gitignore.hook.futurecandy` based off of [perpetualCreations/auto-gitignore](https://github.com/perpetualCreations/auto-gitignore) forked from [Mux-Mastermann/auto-gitignore](https://github.com/Mux-Mastermann/auto-gitignore).
