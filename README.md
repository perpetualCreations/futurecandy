# futurecandy
Linux utility for launching projects in a single command.

Run with `python -m futurecandy` or add a command alias to your shell RC file with `python -m futurecandy.extra` to run with command `futurecandy`.

futurecandy will create directory `.futurecandy` in the user's home directory.
Edit configuration files and hooks there.

## Hooks
Users may add their own hooks, by creating a file in directory `~/.futurecandy/hook`, with file extension `.hook.futurecandy`.

Below is an example hook,
```
[meta]
name = "LICENSE"
description = "Hook for generating LICENSE files."

[exec]
script = "python -m futurecandy.hooks.License {}"
want_path = True
```

Hooks must have a `meta` section with the name of the hook, and its description.
This will appear on the hook selection menu.

Followed is the `exec` section with a command to run, defined with property `script`.

To specify the path to the project directory for the command, include `{}` as a placeholder in the `script` command, which will be replaced with the directory path, and set `want_path` to `True`.

## Acknowledgements
`gitignore.hook.futurecandy` based off of [perpetualCreations/auto-gitignore](https://github.com/perpetualCreations/auto-gitignore) forked from [Mux-Mastermann/auto-gitignore](https://github.com/Mux-Mastermann/auto-gitignore).
