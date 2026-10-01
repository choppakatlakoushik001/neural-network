# neural-network-qec

An early research scaffold for studying decoders for quantum error correction.
The current implementation does not yet contain a neural network. It builds
configurable Stim rotated surface-code memory circuits, samples detector events
and logical observables, and evaluates a PyMatching minimum-weight perfect
matching (MWPM) baseline.

## Setup

The project requires Python 3.12 and uses `uv` with locked Stim, PyMatching,
Sinter, NumPy, pandas, and Matplotlib dependencies. This checkout keeps its
virtual environment outside the OneDrive-synced project folder at
`~/.venvs/neural-network-qec`. The tracked `.envrc` sets that location
automatically for `direnv` users; it can also be exported manually:

```sh
export UV_PROJECT_ENVIRONMENT=~/.venvs/neural-network-qec
uv sync --extra dev
```

The `dev` extra currently declares pytest only. Ruff and basedpyright commands
therefore require those tools to be available separately in the environment
that runs them.

## Direct threshold sweep

Run the direct PyMatching sweep as a package module:

```sh
uv run python -m neural_network_qec.normal_sweep
```

The module evaluates nine logarithmically spaced physical error rates from
`0.001` through approximately `0.0501` at code distances 3, 5, and 7, with the
number of syndrome rounds equal to the distance. For each point, it applies
`p` to data and Clifford depolarization and `10p` to measurement and reset
flips:

- `before_round_data_depolarization`
- `before_measure_flip_probability`
- `after_clifford_depolarization`
- `after_reset_flip_probability`

For each of the 27 `(p, distance)` points it samples 1,000,000 shots, builds a
decomposed detector error model, decodes with PyMatching, and measures logical
observable mismatches. It converts the per-shot logical error rate `L` to the
equivalent per-round rate
`0.5 * (1 - (1 - 2L) ** (1 / rounds))`, stores the results in a pandas
DataFrame, and prints adjacent-distance suppression ratios.

`threshold_plot()` draws the distance curves on log-log axes. It linearly
interpolates sign changes between adjacent curves in log space and reports the
geometric mean of the pairwise crossings as the threshold estimate. The sweep
is unseeded and `plt.show()` opens an interactive plot, so numerical results
vary between runs and the command requires a graphical Matplotlib backend.

## Adaptive Sinter sweep

The separate Sinter workflow can resume a larger adaptive experiment:

```sh
uv run python -m neural_network_qec.sinter_sweep
```

It creates 81 tasks from distances 3, 5, and 7; nine physical error rates from
`0.001` through approximately `0.0200`; and syndrome-round counts of `d`, `2d`,
and `3d`. It uses the same asymmetric `p`/`10p` noise model and PyMatching
decoder, runs with six workers, and stops each task at 1,000,000 shots or 1,000
logical errors. Progress is resumed into
`data/sinter_asymmetric_10x.csv`. The `data/` directory is intentionally ignored
because experiment output can be large.

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
    normal_sweep.py  direct MWPM probability sweep and threshold estimate
    sinter_sweep.py  resumable adaptive Sinter experiment
    viz.py           Stim diagram viewer and threshold plotting helper
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

- `normal_sweep.py` runs at import time, has fixed experiment parameters, and
  has no command-line interface or reproducible seed.
- Its default run samples 27 million shots in total and keeps a one-million-shot
  detector batch in memory for each point. It does not persist the DataFrame or
  calculate confidence intervals.
- `sinter_sweep.py` uses a relative results path, so it must be run from the
  repository root to resume the intended `data/sinter_asymmetric_10x.csv` file.
- The asymmetric noise-model label and output filename are written separately
  from the four numerical noise arguments, so future parameter edits must keep
  them synchronized manually.
- The tracked tests cover package/entry-point integrity only; they do not yet
  test the circuit, decoder, threshold interpolation, or experiment numerics.
- Neural-network training, learned decoding, evaluation, and benchmarking
  against the MWPM baseline are not implemented yet.

## Offline use

After the locked dependencies are installed, circuit construction, sampling,
MWPM decoding, and file-based diagram rendering work locally. A first
installation or uncached dependency update needs access to PyPI, and a push
needs access to GitHub.
