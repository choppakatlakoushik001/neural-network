# Direct-sweep figure and measurements

`normal-sweep-threshold.png` presents the actual 2026-11-11 run of
`neural_network_qec.normal_sweep`; `normal-sweep-results.csv` contains its 27
measured DataFrame rows (`distance`, `physical_p`, `LER_per_round`). It is a
different experiment from the root Sinter batch snapshot.

## Experiment

- Circuit: Stim `surface_code:rotated_memory_z`.
- Decoder: PyMatching minimum-weight perfect matching from the decomposed
  detector error model.
- Distances: 3, 5, 7; syndrome rounds equal distance.
- Sweep: `numpy.logspace(-3, -1.3, 9)`.
- Shots: 1,000,000 per point; 27,000,000 in total.
- Noise: before-round data and after-Clifford depolarization `p`;
  before-measurement and after-reset flips `10p`.
- No seed was supplied; independent reruns will differ.

The module counted logical-observable mismatches and converted per-shot rate
`L` to the equivalent per-round rate
`0.5 * (1 - (1 - 2 * clip(L, 0, 0.5)) ** (1 / rounds))`.
This conversion assumes independent identical logical flips. Near `L = 0.5`,
finite-sample fluctuations and clipping strongly affect the converted rate.

## Reading the crossing

The existing `viz.threshold_plot()` helper linearly interpolates sign changes
between adjacent distance curves in log-log coordinates, then reports the
geometric mean of those pairwise crossings. This run reported `p ≈ 0.00939`.
The figure has no confidence intervals or finite-size extrapolation. Its scope
is these three code sizes under this synthetic noise model; there is no
uniform-noise comparison, hardware validation, or neural-decoder result here.

## Export provenance

The actual module was executed unchanged, with Matplotlib's noninteractive Agg
backend and a capture of its final figure and returned DataFrame. No simulation
parameter or numerical calculation was changed. A presentation export was then
rendered with the same helper and saved measurements: title and axis wording
were clarified, and an overlapping duplicate numerical annotation was removed.
The curves, interpolation, and crossing were retained.

The direct source came from local base commit
`6a9e58a7d48acb5199cc6c2cca8e65092d2ab779` plus its saved comment-spacing edit.
Documentation/comments and formatting added for publication leave these
numerical calculations unchanged.

Installed versions used for the run:

Python 3.12.13; stim 1.16.0, pymatching 2.4.0, numpy 2.5.2, pandas 3.0.5, matplotlib 3.11.1, sinter 1.16.0.
