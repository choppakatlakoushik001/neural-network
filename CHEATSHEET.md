# Neovim cheat sheet — VS Code equivalents

`Space` is the leader key. Where you see `Space e`, that means tap Space, then e.

## The five you need on day one

| Do this | Keys | VS Code equivalent |
|---|---|---|
| Save | `Ctrl+S` | Ctrl+S |
| Run current file | `F5` | F5 / Run |
| Open file by name | `Ctrl+P` | Ctrl+P |
| Toggle file tree | `Space e` | Ctrl+B |
| Quit Neovim | `:qa` then Enter | close window |

`Ctrl+S` and `F5` work from *any* mode, including while typing. Everything
else assumes you are in NORMAL mode — press `Esc` first if unsure.

## Modes (the thing VS Code doesn't have)

| Mode | Enter with | What it's for |
|---|---|---|
| NORMAL | `Esc` | navigating, commands. **Default.** |
| INSERT | `i` | typing text. This is "normal" VS Code. |
| VISUAL | `v` | selecting text |
| COMMAND | `:` | running `:w`, `:q`, etc. |

The bottom-left of the screen always tells you which mode you're in.

## File tree (neo-tree)

Move focus to the tree with `Ctrl+H`, then:

| Key | Action |
|---|---|
| `a` | **create new file** — type `foo.py` and Enter |
| `a` + trailing `/` | create a folder — type `models/` and Enter |
| `d` | delete (asks first) |
| `r` | rename |
| `c` / `m` | copy / move |
| `Enter` | open file, or expand/collapse folder |
| `s` | open in a vertical split |
| `S` | open in a horizontal split |
| `H` | show/hide hidden dotfiles |
| `R` | refresh the tree |
| `?` | full list of tree keys |
| `q` | close the tree |

**Creating a `.py` file:** press `a`, type the full name including the
extension (`train.py`), press Enter. The extension is what tells Neovim to turn
on Python highlighting, completion, and error checking.

New Python files belong in `src/neural_network_qec/`. New tests go in `tests/`
and must be named `test_*.py` or pytest won't find them.

## Moving around

| Key | Action |
|---|---|
| `h` `j` `k` `l` | left, down, up, right |
| `w` / `b` | forward / back one word |
| `0` / `$` | start / end of line |
| `gg` / `G` | top / bottom of file |
| `Ctrl+D` / `Ctrl+U` | half page down / up |
| `{` / `}` | previous / next blank line |
| `/text` Enter | search forward; `n` next, `N` previous |
| `Esc` | clear the search highlight |

## Editing

| Key | Action |
|---|---|
| `i` / `a` | insert before / after cursor |
| `o` / `O` | new line below / above, and start typing |
| `x` | delete character |
| `dd` | delete (cut) line |
| `yy` | copy line |
| `p` / `P` | paste after / before |
| `u` | undo |
| `Ctrl+R` | redo |
| `v` then `y` | select, then copy |
| `>>` / `<<` | indent / outdent line |
| `J` / `K` in VISUAL | move selected lines down / up |
| `ciw` | change the word under the cursor |

## Splits and tabs

| Key | Action |
|---|---|
| `Ctrl+H` `Ctrl+J` `Ctrl+K` `Ctrl+L` | move between splits |
| `:vsplit` / `:split` | new vertical / horizontal split |
| `H` / `L` | previous / next open file (the tabs up top) |
| `Space x` | close the current tab |
| `Space b` | list open files and pick one |

## Code intelligence (basedpyright + ruff)

| Key | Action | VS Code equivalent |
|---|---|---|
| `gd` | go to definition | F12 |
| `gr` | find references | Shift+F12 |
| `gi` | go to implementation | Ctrl+F12 |
| `K` | hover docs | hover with mouse |
| `Space rn` | rename symbol everywhere | F2 |
| `Space ca` | code action / quick fix | Ctrl+. |
| `Space fm` | format the file | Shift+Alt+F |
| `]d` / `[d` | next / previous error | F8 |
| `Space d` | list all errors in this file | Problems panel |
| `Space ih` | toggle inlay type hints | — |

Completion appears as you type. `Tab` accepts it, `Ctrl+N` / `Ctrl+P` cycle
through the options.

## Searching the project

| Key | Action |
|---|---|
| `Ctrl+P` or `Space f` | find file by name |
| `Space g` | grep — search file *contents* |
| `Space h` | search Neovim's own help |

## Running things

| Key | Action |
|---|---|
| `F5` | run current file, output in a split inside Neovim |
| `Space r` | same as F5 (normal mode only) |
| `Space R` | run in the *next existing* tmux pane |
| `q` | close the Neovim output window |

### One tmux pane per file

These open a **new** pane each time, so several files can run side by side,
each keeping its own scrollback.

| Key | Action | Where the cursor ends up |
|---|---|---|
| `Space tr` | run this file, new pane **right** | stays in the editor |
| `Space tR` | run this file, new pane **below** | stays in the editor |
| `Space tt` | `pytest -v` in a new pane | stays in the editor |
| `Space tl` | `ruff check .` in a new pane | stays in the editor |
| `Space tv` | bare shell, split right | moves to the shell |
| `Space ts` | bare shell, split below | moves to the shell |

The runners deliberately leave you in the code so you can keep typing while the
output scrolls beside you. The bare shells take focus, because you opened one
to type in it.

Every one of these panes starts at the project root with `.venv/bin` ahead on
`PATH`, so `python`, `pytest` and `qec` are the project's versions — no
`activate` step, no `uv run` prefix.

The pane stays open after the program finishes, so tracebacks stay on screen
and Up-Arrow re-runs the last command. Close a pane with `exit` or `Ctrl+D`.

Moving between panes once they exist:

| Key | Action |
|---|---|
| `Ctrl+B` then arrow key | move to the pane in that direction |
| `Ctrl+B` then `o` | cycle to the next pane |
| `Ctrl+B` then `z` | zoom the current pane full-screen (again to unzoom) |
| `Ctrl+B` then `x` | kill the current pane |
| `Ctrl+B` then `Space` | cycle through layouts |

`Ctrl+B` then `z` is the one worth memorising — zoom a runner pane to read a
long traceback, press it again to go back to the split view.

The runner uses `.venv/bin/python`, which is a symlink to
`~/.venvs/neural-network-qec`. That's the interpreter with numpy installed.

For the whole test suite, drop to a shell instead:

```sh
uv run pytest             # all tests
uv run pytest -v          # verbose, one line per test
uv run ruff check .       # lint the project
uv run ruff format .      # format the project
uv run qec --shots 5      # run the CLI
```

## Adding a dependency

```sh
uv add torch              # installs and records it in pyproject.toml
uv add --dev pytest-cov   # dev-only dependency
uv sync                   # reinstall everything from the lockfile
```

`uv add` is the only command here that needs internet.

## Saving and quitting

| Command | Action |
|---|---|
| `Ctrl+S` or `Space w` | save |
| `:w` | save |
| `:q` | quit this split |
| `:wq` | save and quit |
| `:qa` | quit everything |
| `:q!` | quit, **throwing away unsaved changes** |

If Neovim refuses to quit, it's because a file is unsaved. Either `:wq` to keep
the changes or `:q!` to discard them.

## Git

Committing is local and works with no internet. Line-level markers in the
gutter come from gitsigns.

```sh
git status
git add -A
git commit -m "message"
git push          # this one needs internet
```

Or use GitHub Desktop on the Windows side — it's the same repository.

## tmux (the window manager around Neovim)

`Ctrl+B` is tmux's prefix — press it, release, then the next key.

| Key | Action |
|---|---|
| `Ctrl+B` then `c` | new window |
| `Ctrl+B` then a number | jump to that window |
| `Ctrl+B` then `n` / `p` | next / previous window |
| `Ctrl+B` then `\|` | split left/right |
| `Ctrl+B` then `-` | split top/bottom |
| `Ctrl+B` then `d` | detach (everything keeps running) |
| `tmux attach` | come back |

Because tmux owns `Ctrl+B`, that key never reaches Neovim — which is why the
sidebar toggle is `Space e` rather than VS Code's `Ctrl+B`.
