Either with args or interactive mode,

1. Point to a parent directory for the child project directory, or load from configuration.
2. Request name, required.
3. Request whether project directory should be initialized with Git, or load from configuration.
   1. If yes, request Git remote(s) to initialize with, or load from configuration.
4. Request whether user hooks should be ran, or load from configuration.
   1. Request whther user hooks marked "run-expicitly-only" should also be ran, or load from configuration.
5. Request code editor to launch, or load from configuration.
6. Exit.

Extra hooks,

1. Auto-generate .gitignore.
2. Auto-generate venv.
3. Install to venv mypy, flake8...
4. NPM and JavaScript frameworks
5. Set LICENSE.
6. Structure templates, some of the concepts above can be integrated into it.
