# neural-network-qec

Neural network decoders for quantum error correction.

## Setup

The virtualenv lives **outside** this folder, at `~/.venvs/neural-network-qec`.
This repo sits in a OneDrive-synced Windows directory where small-file writes
are ~50ms each; a virtualenv is thousands of files, so keeping it on the Linux
side makes installs fast and stops OneDrive syncing packages it shouldn't.

`uv` picks this up automatically from `.envrc`, or export it yourself:

```sh
export UV_PROJECT_ENVIRONMENT=~/.venvs/neural-network-qec
uv sync --extra dev
```

## Usage

```sh
uv run qec --shots 5      # run the CLI
uv run pytest             # run the tests
uv run ruff check .       # lint
```

## Layout

```
src/neural_network_qec/
    decoder.py     model / decoding logic
    cli.py         command line entry point
tests/
    test_decoder.py
```

## Offline

Everything except `uv add` (which fetches from PyPI) and `git push` works with
no internet. Editing, running, testing, and committing are all local.
