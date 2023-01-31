# max-temps


Development setup uses devcontainer for use with Github Codespaces.

For prod, split out the dev dependencies into seperate Dockerfile/use compose? Possibly also run as non-root user.


To start a terminal in the codespace from VSCode, use the + button to add a new bash session.

Run tests with `python -m pytest`, not `pytest` because software is just generally a mess. Seriously why do I still have to google relative imports every time?