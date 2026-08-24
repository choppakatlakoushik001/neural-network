# neural-network-qec

An early research scaffold for studying neural-network decoders for quantum
error correction.
The current saved implementation does not yet contain a neural network or a
decoder.
It builds configurable Stim rotated surface-code memory circuits and samples
their detector events.

## Setup

The project requires Python 3.12 and uses `uv` with a locked NumPy and Stim
environment.
This checkout keeps its virtual environment outside the OneDrive-synced project
folder at `~/.venvs/neural-network-qec`.
The tracked `.envrc` sets that location automatically for `direnv` users; it can
also be exported manually:

```sh
export UV_PROJECT_ENVIRONMENT=~/.venvs/neural-network-qec
uv sync --extra dev
```

The `dev` extra currently declares pytest only.
Ruff and basedpyright commands therefore require those tools to be installed
separately in the environment that runs them.

## Current usage

Run the saved sampling script as a package module:

```sh
uv run python -m neural_network_qec.shots
```

It constructs a distance-3, three-round rotated memory-Z circuit with a `0.04`
before-round data-depolarization probability and a `0.01` pre-measurement flip
probability, then prints five randomly sampled detector-event rows.

The same behavior is available as a Python API:

```python
from neural_network_qec.circuit import circuit_info

circuit = circuit_info(
    rounds=3,
    distance=3,
    before_round_data_depolarization=0.04,
    before_measure_flip_probability=0.01,
)
detector_events = circuit.sample_detectors(shots=5)
```

For this configuration, `detector_events` is a Boolean NumPy array with shape
`(5, 24)`.
Sampling is stochastic, so the values change between runs.

## Layout

```text
src/neural_network_qec/
    __init__.py    package version metadata
    circuit.py     Stim circuit configuration and detector sampling
    shots.py       fixed five-shot sampling script
logs.md            evidence-based development journal
pyproject.toml     package, dependency, and tool configuration
uv.lock            reproducible dependency lock
```

Generated diagrams under `diagrams/`, root scratch files `test.py` and
`test_1.py`, virtual environments, bytecode, and tool caches are intentionally
ignored and are not part of the tracked project snapshot.

## Current limitations

- The tracked `qec` console entry still targets the removed
  `neural_network_qec.cli:main` module and does not run.
- There are currently no tracked tests, so pytest collects no tests.
- The current source does not pass the configured Ruff lint and format checks.
- Decoder logic, neural-network training, evaluation, and benchmarking are not
  implemented yet.
- `shots.py` runs its fixed sample at module import time and does not accept
  command-line options.

## Offline use

After the locked dependencies are installed, circuit construction and sampling
work locally.
A first installation or uncached dependency update needs access to PyPI, and a
push needs access to GitHub.
