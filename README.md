# neural-network-qec

An early research scaffold for studying decoders for quantum error correction.
The current implementation does not yet contain a neural network. It builds
configurable Stim rotated surface-code memory circuits, samples detector events
and logical observables, and evaluates a PyMatching minimum-weight perfect
matching (MWPM) baseline.

## Setup

The project requires Python 3.12 and uses `uv` with locked NumPy, PyMatching,
and Stim dependencies. This checkout keeps its virtual environment outside the
OneDrive-synced project folder at `~/.venvs/neural-network-qec`. The tracked
`.envrc` sets that location automatically for `direnv` users; it can also be
exported manually:

```sh
export UV_PROJECT_ENVIRONMENT=~/.venvs/neural-network-qec
uv sync --extra dev
```

The `dev` extra currently declares pytest only. Ruff and basedpyright commands
therefore require those tools to be available separately in the environment
that runs them.

## Current experiment

Run the saved experiment as a package module:

```sh
uv run python -m neural_network_qec.shots
```

The module sweeps code distances 3, 5, and 7, with the number of syndrome
rounds set equal to the distance. It assigns `p = 0.005` to all four configured
Stim noise controls:

- `before_round_data_depolarization`
- `before_measure_flip_probability`
- `after_clifford_depolarization`
- `after_reset_flip_probability`

For each distance it samples 1,000,000 shots, builds a decomposed detector error
model, decodes the detector batches with PyMatching, and prints the number of
observable-prediction mismatches and the raw logical error rate per shot. It
then divides that rate by the number of rounds, collects the normalized
per-round rates, and prints the adjacent-distance ratios for distances 3 to 5
and 5 to 7 as suppression factors. Sampling is unseeded, so the numerical
results vary between runs.

The same pipeline is available through the Python API:

```python
import numpy as np
import pymatching

from neural_network_qec.circuit import circuit_info

circuit = circuit_info(
    rounds=3,
    distance=3,
    before_round_data_depolarization=0.005,
    before_measure_flip_probability=0.005,
    after_clifford_depolarization=0.005,
    after_reset_flip_probability=0.005,
)
detector_events, observables = circuit.sample_detectors(shots=10)
model = circuit.detector_error_model()
matcher = pymatching.Matching.from_detector_error_model(model)
predictions = matcher.decode_batch(detector_events)
logical_error_rate = np.mean(np.any(predictions != observables, axis=1))
```

For the distance-3, three-round configuration, ten shots produce Boolean
detector and observable arrays with shapes `(10, 24)` and `(10, 1)`; PyMatching
returns predictions with shape `(10, 1)`.

## Circuit diagrams

`circuit_info.circuit_diagram()` renders a Stim diagram to a timestamped SVG or
HTML file and tries to open it with the platform's browser tooling:

```python
path = circuit.circuit_diagram(kind="timeline-svg", name="circuit")
```

Set `QEC_VIZ_NO_OPEN=1` to write without opening a browser, and set
`QEC_VIZ_DIR` to choose the output directory. Otherwise, output is written
under a temporary `qec-viz` directory (or the Windows temporary directory when
it can be resolved from WSL). Generated diagrams are local output and are not
tracked.

## Layout

```text
src/neural_network_qec/
    __init__.py    package version metadata
    circuit.py     Stim circuit, sampling, diagram, and error-model API
    shots.py       MWPM distance sweep, normalized rates, and suppression ratios
    viz.py         portable file-based Stim diagram viewer
tests/
    test_packaging.py  package and declared-entry-point regression checks
logs.md            evidence-based development journal
pyproject.toml     package, dependency, and tool configuration
uv.lock            reproducible dependency lock
```

Generated diagrams under `diagrams/`, root scratch files `test.py` and
`test_1.py`, virtual environments, bytecode, and tool caches are intentionally
ignored and are not part of the tracked project snapshot.

## Current limitations

- `shots.py` runs at import time, has fixed experiment parameters, and has no
  command-line interface or reproducible seed.
- Its default run samples three million shots in total and keeps large batches
  in memory one distance at a time.
- The one-probability distance sweep can indicate whether error suppression
  improves with distance at `p = 0.005`, but its two adjacent-distance ratios
  cannot locate a threshold. The script does not persist results, compute
  uncertainty, or generate a threshold plot.
- The tracked tests cover package/entry-point integrity only; they do not yet
  test the circuit, decoder, or experiment numerics.
- Neural-network training, learned decoding, evaluation, and benchmarking
  against the MWPM baseline are not implemented yet.

## Offline use

After the locked dependencies are installed, circuit construction, sampling,
MWPM decoding, and file-based diagram rendering work locally. A first
installation or uncached dependency update needs access to PyPI, and a push
needs access to GitHub.
