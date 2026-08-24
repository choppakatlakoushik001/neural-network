# Development log

Times use `America/New_York`. This journal is evidence-based: it records Git
history, saved filesystem state, validation output, and explicit project
conversation. It cannot reconstruct unsaved editor buffers, every keystroke,
or commands for which no transcript remains.

## 2026-08-11 (EDT)

### 23:06 — Initial project scaffold committed

- Created commit `6a1541b` (`Initial commit: project scaffold for neural
  network QEC decoders`).
- Added the Python 3.12 package metadata, external virtual-environment setup,
  NumPy dependency, lockfile, and source layout.
- Added the `qec` command, which samples placeholder syndrome bitstrings and
  reports their Hamming weight through `syndrome_weight`.
- Added two unit tests for empty and triggered syndromes.
- Added the initial README and ignore rules for environments, caches, builds,
  datasets, and model artifacts.
- No preserved validation output is available for this date, so this log does
  not claim that tests or lint ran before the commit.

## 2026-08-13 (EDT)

### 11:10 — Local scratch file saved

- Saved `test_1.py` containing a single `hello world` print. It was never added
  to Git and is classified as a local scratch experiment.

### 11:15 — Neovim workflow documentation committed

- Created commit `a702470` (`Add Neovim cheat sheet; fix .venv gitignore
  rule`).
- Added `CHEATSHEET.md` with the project's Neovim modes, file-tree operations,
  LSP navigation, test/lint commands, tmux runner keys, dependency workflow,
  and Git basics.
- Changed `.gitignore` from a directory-only `.venv/` rule to `.venv`, so the
  symlink to `~/.venvs/neural-network-qec` also stays untracked.
- The commit records Claude Opus 5 as a co-author.
- No preserved validation output is available for this date.

## 2026-08-14 (EDT)

### 15:59–17:04 — Stim visualization work saved

- Updated `uv.lock` with Stim 1.16.0 and its NumPy dependency at 15:59.
- Saved `viz.py` at 16:36. It creates a rotated memory-Z surface-code circuit
  and prints either `timeline-text` or `detslice-text`, with tick, distance,
  round, and noise controls.
- Updated `pyproject.toml` at 16:51 to declare `stim>=1.16.0` directly. A local
  basedpyright path for the private `vizshow` helper was also present in the
  saved diff; it was later removed from the publication snapshot because it
  was machine-specific.
- Saved `diagrams.py` at 17:04. It renders five SVG diagram types and one ASCII
  timeline for a distance-3, three-round circuit with 0.005 depolarizing noise.
- Six generated outputs appeared under `diagrams/` at 17:04: five SVG files
  and `timeline.txt` (645,294 bytes total). Their names and timestamps match
  the generator's outputs; no command transcript survives to prove the exact
  invocation.

## 2026-08-18 (EDT)

### 14:05 — Browser visualization scratch experiment present

- The current saved `test.py` constructs a distance-3, three-round Stim circuit,
  samples 1,000 detector shots, and calls the private `vizshow` browser helper.
- Its current filesystem timestamp is 14:05 on August 18. An earlier version
  may have existed, but the available repository evidence does not support the
  previous journal claim that this exact file was saved on August 14 at 21:59.
- The file is an unguarded experiment outside pytest's configured `tests/`
  directory. It remains ignored and is not part of the publication snapshot.

### 12:08–12:14 — Local file-move workflow discussed with Claude

- Connected the Claude session to the local `neural-network` repository and
  asked how to move Python files locally.
- Reviewed `mv <file> <folder>/`, `git mv` for tracked files, trailing-slash
  safety, import-path changes, paths based on `__file__`, stale bytecode, and
  pytest's `tests/`/`test_*.py` collection rules.
- Confirmed in the transcript that `viz.py`, `diagrams.py`, `test.py`, and
  `test_1.py` were untracked. No file move was shown in the transcript.

### 12:18–12:29 — Repository and publication review

- Located the project from the tmux window named `neural-network`: its left
  pane was running Neovim at
  `/mnt/c/Users/chopp/OneDrive/Documents/GitHub/neural-network`.
- Verified branch `main` at `a702470`, with no staged changes, upstream, or Git
  remote.
- Reviewed both existing commits, every saved diff, all untracked source and
  generated files, the README, package configuration, source, tests, and the
  relevant Claude transcript.
- Confirmed the authenticated GitHub account as `choppakatlakoushik001` with
  `gh-axi`. None of the nine accessible repositories matched this project, so
  a destination repository name and visibility still require an explicit
  choice before any remote can be configured.

### 12:29–12:43 — Publication-quality local snapshot prepared

- Chose `diagrams.py` and `viz.py` as reusable source. Kept all generated
  `diagrams/` files plus `test.py` and `test_1.py` local.
- Added narrow ignore rules for those generated and scratch paths; no local
  file was deleted.
- Removed the machine-specific basedpyright `extraPaths` setting used only by
  the private scratch helper.
- Added literal types for Stim diagram kinds, resolving two basedpyright type
  errors.
- Formatted `viz.py` and made `diagrams.py` handle a missing optional `vizopen`
  command by printing the output path instead of raising `FileNotFoundError`.
- Updated the README with verified Stim usage, visualization options, generated
  output behavior, project layout, and accurate offline-install limits.
- Created this development log with the history and evidence available today.

### Validation and failures handled

- Initial `uv` checks inside the review sandbox could not create lock files in
  `~/.cache/uv`; the same checks were rerun with the project's normal local
  environment.
- `uv lock --check` — passed; resolved 9 packages.
- `uv run ruff check --no-cache src tests diagrams.py viz.py` — passed.
- `uv run ruff format --check --no-cache src tests diagrams.py viz.py` —
  passed; all 6 Python files were formatted.
- `uv run basedpyright` — passed with 0 errors, warnings, or notes.
- `uv run pytest -q` — passed, 2 tests.
- `uv run qec --shots 2` — passed; printed weights 0 and 1.
- `uv run python viz.py detslice 3 -r 1` — passed and rendered a text detector
  slice.
- Importing `diagrams` and rendering its in-memory `timeline-svg` — passed;
  produced an 84,069-character SVG string without writing or opening files.
- The visualization helpers do not yet have dedicated automated tests; their
  coverage in this review is limited to type, lint, formatting, and smoke
  checks.

### 16:03–16:22 — Decoder overwrite and silent SVG result diagnosed

- The saved `decoder.py` was overwritten with a Stim memory-Z circuit
  experiment. This removed `syndrome_weight`, while `cli.py` and the committed
  tests still imported it.
- Claude identified the resulting pytest collection failure and explained that
  placing scratch work in an imported package module had broken the existing
  API contract.
- The circuit was constructed at import time and
  `circuit.diagram("timeline-svg")` returned an SVG helper that was neither
  stored, printed, nor written. The process therefore exited successfully but
  displayed nothing.
- At 16:21 the user explicitly asked why exit status 0 did not display a
  diagram. The discussion distinguished successful execution from presenting
  a returned value and noted that terminals do not render raw SVG.
- No transcript records a final restore-versus-redesign choice on this date.

### Unresolved publication item

- The local repository still has no remote or upstream, and GitHub has no
  matching existing repository. Nothing has been staged, committed, or pushed.
  Repository name, visibility, and explicit authorization to create/configure
  that destination are required before a push preview can be finalized.

## 2026-08-19 (EDT)

### 16:25 — Test-file visualization experiment saved

- `tests/test_decoder.py` was saved with a memory-X Stim circuit, a private
  `vizshow` import, and a text-diagram print attempt.
- The file had an unexpected leading indent, no test functions or assertions,
  and no longer exercised the decoder API.
- The exact command or editor sequence that removed the previously reviewed
  root `viz.py` and `diagrams.py` files is not recorded. They were absent when
  the publication review began, while their generated local output remained.

### Afternoon — Fresh publication review and destination setup

- A bare `push` triggered a new guarded review; it did not authorize staging,
  committing, or pushing.
- The expected tmux window name was no longer present. Two panes resolved to
  the same repository, and the user explicitly confirmed tmux `kunchen:5`,
  left pane `%7`, as the intended Neovim target.
- Verified `main` at `a702470` with no staged changes, upstream, or remote.
- Initial checks found `uv lock --check` passing, while pytest failed on the
  test-file `IndentationError`, `qec --shots 2` failed because
  `syndrome_weight` was missing, and `git diff --check` reported the malformed
  Python-file endings. Ruff and basedpyright were unavailable in the first
  read-only sandbox attempt because uv could not write its cache lock.
- The user authorized a public GitHub destination. At 17:31, `gh-axi` created
  `choppakatlakoushik001/neural-network`; GitHub reported an empty public
  repository with default-branch metadata `main`.
- Added the exact HTTPS repository URL as local remote `origin`. No remote
  branch or upstream was created, and nothing was pushed.

### Minimal repair authorized

- The user chose the recommended narrow repair rather than publishing the
  broken hybrid state.
- Restored the `syndrome_weight` API required by `cli.py` and existing users.
- Replaced the discarded import-time rendering expression with
  `surface_code_timeline_svg()`, which returns the generated SVG string to its
  caller without opening a browser or writing files.
- Repaired `tests/test_decoder.py`: restored both syndrome tests, removed the
  undeclared private helper, and added an assertion that the Stim helper
  returns SVG markup.
- Updated the README to document only the implemented API and removed commands
  for the now-absent root visualization scripts.

### 20:34–20:36 — Repaired snapshot validated

- `uv lock --check` — passed; resolved 9 packages.
- `uv run ruff check --no-cache src tests` — passed.
- `uv run ruff format --check --no-cache src tests` — passed; all 4 Python
  files were formatted.
- `uv run basedpyright` — passed with 0 errors, warnings, or notes.
- `uv run pytest -q` — passed, 3 tests.
- `uv run qec --shots 2` — passed; printed weights 0 and 1.
- Directly called `surface_code_timeline_svg()` and checked both SVG tags —
  passed; the returned string was 44,027 characters.
- `git diff --check` — passed.
- Credential-pattern scans of the intended files and both existing commits —
  passed with no matches; no intended file exceeded 1 MiB.
- Refreshed `origin/main` with `git ls-remote`; the authorized public
  destination remained empty and no remote branch existed.
- Nothing was staged, committed, or pushed during preparation.

### 21:48 — Test coverage removed after validation

- `tests/test_decoder.py` was saved as a one-byte blank file, removing the three
  tests that had passed earlier that evening.
- No commit captured the repaired source or its validation state. The 20:34–
  20:36 results above describe a transient worktree snapshot; they do not apply
  to the later August 19 files or to the current branch.

## 2026-08-20 (EDT)

### 00:18–00:44 — Research sequence and noise methodology discussed

- The project conversation recorded a proposed progression from Stim circuit
  construction and detector samples to an MWPM baseline, threshold sweep,
  dataset split, hand-written MLP, and head-to-head logical-error-rate
  comparison. This was planning context, not implemented repository behavior.
- The discussion distinguished the separate Stim noise controls rather than
  treating a physical error rate as one undocumented scalar. It called out
  `after_clifford_depolarization`,
  `before_round_data_depolarization`,
  `before_measure_flip_probability`, and
  `after_reset_flip_probability` as experiment-defining choices that must be
  logged explicitly.
- The session adopted a project-specific hand-coding workflow: the user writes
  the implementation, while Claude explains APIs and reviews saved code,
  algorithms, rigor, and coding habits.

### 14:43–15:58 — Broken package state and browser visualization reviewed

- A fresh code scan found that the previously repaired decoder API and tests
  were no longer present on disk, while `cli.py` still expected
  `syndrome_weight`. The journal's earlier validation was therefore stale.
- Later in the same session, `decoder.py` had again become an import-time Stim
  experiment with browser-display calls. The private `vizshow` helper was found
  at a machine-local path and was not a declared package dependency.
- The generated SVG and 3-D HTML outputs were inspected. The SVG was
  well-formed; the 3-D file depended on browser-loaded JavaScript modules.
- Browser automation could not attach to the user's Windows Brave session, so
  no claim was made about the visible tab. Windows file-association evidence
  showed that SVG and HTML files opened through Microsoft Edge instead of the
  Brave window being watched.
- None of this browser-specific experiment remains in the current tracked
  source. The related root `test.py` and generated `diagrams/` outputs remain
  local and ignored.

## 2026-08-23 (EDT)

### 17:28–17:46 — Repository state and Stim tick behavior reviewed

- Git still showed `a702470` as the latest commit. The uncommitted decoder
  experiment had changed again, using a distance-2, two-round circuit, and the
  previous repaired snapshot was no longer recoverable from a commit.
- On that saved circuit, `num_ticks` was 14 and `num_qubits` was 13.
- `c.diagram("timeline-text", tick=5)` was verified to raise a `ValueError`
  because timeline diagrams do not accept the `tick` selector.
- `timeslice-svg` and `detslice-*` were identified as the diagram families that
  accept tick selections. A `timeslice-svg` call for `range(3, 6)` returned a
  4,683-character SVG during the conversation; no generated file from that
  check was added to Git.

### 21:02–23:52 — Package imports and circuit class iterated

- Intermediate saved states renamed the original decoder work toward
  `main.py`, renamed the old CLI to `shots.py`, and introduced a temporary
  `imports.py` using star imports.
- Direct script execution found the bare `imports` module only because the
  script directory was placed on `sys.path`; importing the same file as a
  package raised `ModuleNotFoundError`. The temporary shared-import module was
  subsequently removed in favor of an explicit package import.
- Moving executable Stim statements into a class body did not remove import-time
  side effects. The implementation then moved circuit construction into
  `__init__` and renamed the module to `circuit.py`.
- Review cycles identified a constructor assignment embedded inside the Stim
  call, a forbidden value return from `__init__`, a mistaken `==` comparison,
  values built and discarded as locals instead of stored on `self`, and calls
  to Stim sampler methods on the wrapper object rather than its circuit.
- By the end of the date, the implementation stored the four constructor
  parameters and the generated Stim circuit on the instance, but further
  sampling fixes were still in progress.

## 2026-08-24 (EDT)

### 00:09–00:38 — Detector-sampling implementation reached a runnable state

- Removed trailing commas that had silently stored the four configuration
  values as one-element tuples. The current instance now retains integer
  `rounds` and `distance` values and floating-point noise probabilities.
- Added `sample_detectors(shots)`, which compiles a detector sampler from the
  stored circuit and returns the sampled detector-event array.
- Renamed the class from `circuit_diagram` to `circuit_info`, reflecting that it
  stores circuit configuration and samples rather than rendering diagrams.
- Several `shots.py` iterations called `compile_sampler`, referenced a removed
  `sampler` local, or invoked `sample_detectors` without an instance. The final
  saved call is `c.sample_detectors(5)`.
- The paired Claude review verified `c.sample_detectors(3).shape == (3, 24)`
  before the final script correction. The later guarded publication review
  independently verified the current module and API, as recorded below.

### 00:39–00:56 — Guarded publication review and documentation synchronization

- Rediscovered the only accessible neural-network-associated editor surface and
  resolved its Git root to this local checkout. Verified branch `main` at
  `a702470`, with no upstream.
- At 00:46, while the review was reading the repository, the index changed to
  stage deletion of `CHEATSHEET.md` and `tests/test_decoder.py`.
- The same index retained pure renames from `decoder.py` to `circuit.py` and
  from `cli.py` to `shots.py`; the substantive destination-file edits remained
  unstaged. The reviewer did not create, replace, stage, or unstage any of those
  changes.
- The first review fingerprint was invalidated and the complete saved local
  state was reviewed again after it stabilized.
- Reviewed the full two-commit history, the staged and unstaged patches, package
  configuration, current source, deleted tests and cheat sheet, ignored local
  files, generated outputs, and the paired Claude conversation. Local files and
  executable behavior were treated as authoritative; conversation was used only
  for intent and chronology.
- Rewrote `README.md` to describe the current detector-sampling API and module
  command, the exact fixed configuration in `shots.py`, the tracked layout,
  ignored local artifacts, and the current absence of a working `qec` entry
  point, tests, Ruff compliance, decoder, neural network, and benchmark.
- Updated this journal through August 24 and qualified the earlier validation
  claims that later saved edits had invalidated.

### Validation of the current saved implementation

- `uv lock --check` — passed; resolved 9 packages.
- Initial `uv run` checks could not create temporary lock files in the sandboxed
  `~/.cache/uv`. The same repository-derived checks were rerun directly with
  the configured project environment and installed tools.
- `ruff check --no-cache src` — failed with `I001` for import formatting and
  `E501` for the 124-character constructor line.
- `ruff format --check --no-cache src` — failed; `circuit.py` and `shots.py`
  would be reformatted.
- `basedpyright` — passed with 0 errors, warnings, or notes.
- `.venv/bin/pytest -q -p no:cacheprovider` — failed with exit code 5 because
  no tests were found; pytest also warned that the configured `tests` path had
  no files.
- `.venv/bin/python -m neural_network_qec.shots` — passed and printed five
  randomly sampled detector rows.
- A direct API smoke constructed `circuit_info(3, 3, 0.04, 0.01)` and sampled
  two shots — passed with shape `(2, 24)`, Boolean dtype, rounds 3, and distance
  3.
- `.venv/bin/qec --shots 2` — failed because the console entry still imports
  the removed `neural_network_qec.cli` module.
- `git diff --check` and `git diff --cached --check` — passed.
- The ignored `diagrams/` directory contains six generated files totaling
  645,294 bytes. `test.py`, `test_1.py`, `.venv`, bytecode, and tool caches also
  remain local and excluded.
- No source, test, entry-point, staging, commit, or push repair was performed by
  the guarded publication review.
