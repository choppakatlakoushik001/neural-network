"""Portable viewer for stim diagrams.

A plain Python script has no display system, so ``print()`` on a stim diagram
falls back to text. This module supplies the missing half: it renders the
diagram to a file and opens it in the system browser.

    from neural_network_qec.viz import show
    show(circuit.diagram("timeline-svg"), name="timeline")

Only the standard library is used, so it works on WSL, Linux, macOS and
Windows. If no opener can be found it prints the path instead of raising --
looking at a diagram must never be able to fail a script.

Set ``QEC_VIZ_NO_OPEN=1`` to write without opening (CI, or batch renders).
Set ``QEC_VIZ_DIR`` to choose the output directory.
"""

from __future__ import annotations

import os
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import webbrowser

__all__ = ["show", "source", "outdir"]

_TEXT_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body style="background:#111;color:#eee;margin:0">
<pre style="font:12px/1.25 ui-monospace,Menlo,Consolas,monospace;
            padding:16px">{body}</pre>
</body></html>
"""


def _is_wsl() -> bool:
    return "microsoft" in platform.uname().release.lower()


def _windows_temp() -> pathlib.Path | None:
    """Windows %TEMP% seen from WSL, or None if it cannot be resolved.

    Under WSL a Linux path translates to \\\\wsl.localhost\\..., which Windows
    browsers open unreliably. Writing to a real C:\\ path avoids that entirely.
    """
    cmd = "/mnt/c/Windows/System32/cmd.exe"
    if not os.access(cmd, os.X_OK) or not shutil.which("wslpath"):
        return None
    try:
        win = subprocess.run(
            [cmd, "/c", "echo %TEMP%"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        ).stdout.strip()
        if not win or "%TEMP%" in win:
            return None
        linux = subprocess.run(
            ["wslpath", "-u", win],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    path = pathlib.Path(linux) if linux else None
    return path if path and path.is_dir() else None


def outdir() -> pathlib.Path:
    """Directory diagrams are written to. Read at call time, not import time."""
    env = os.environ.get("QEC_VIZ_DIR")
    if env:
        return pathlib.Path(env)
    base = _windows_temp() if _is_wsl() else None
    return (base or pathlib.Path(tempfile.gettempdir())) / "qec-viz"


def source(obj) -> str:
    """Return the raw source of a stim diagram (SVG, HTML, or text).

    Every stim ``_DiagramHelper`` stringifies to its own source, so ``str`` is
    the supported door -- its ``_repr_svg_`` / ``_repr_html_`` hooks are
    private and exist for Jupyter.
    """
    return obj if isinstance(obj, str) else str(obj)


def _as_page(text: str) -> tuple[str, str]:
    """Return (suffix, body) for something a browser can render."""
    stripped = text.lstrip()
    if stripped.startswith(("<svg", "<?xml")):
        return ".svg", text
    if stripped.startswith("<"):
        return ".html", text
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ".html", _TEXT_PAGE.format(title="diagram", body=escaped)


def _launch(path: pathlib.Path) -> bool:
    """Best-effort open. Returns True if an opener was actually launched."""
    # WSL first: sys.platform is "linux" here and xdg-open exists, but it
    # cannot reach a Windows browser. explorer.exe must be called by absolute
    # path with a translated argument, and it exits non-zero even on success.
    if _is_wsl():
        explorer = "/mnt/c/Windows/explorer.exe"
        if os.access(explorer, os.X_OK) and shutil.which("wslpath"):
            win = subprocess.run(
                ["wslpath", "-w", str(path)],
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            ).stdout.strip()
            if win:
                subprocess.run(
                    [explorer, win], check=False, capture_output=True, timeout=20
                )
                return True

    try:
        if sys.platform == "darwin" and shutil.which("open"):
            subprocess.run(
                ["open", str(path)], check=False, capture_output=True, timeout=20
            )
            return True
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]  # noqa: S606
            return True
        if shutil.which("xdg-open") and not _is_wsl():
            subprocess.run(
                ["xdg-open", str(path)], check=False, capture_output=True, timeout=20
            )
            return True
        return webbrowser.open(path.resolve().as_uri())
    except (OSError, subprocess.SubprocessError):
        return False


def show(obj, name: str = "diagram", open_it: bool = True) -> pathlib.Path:
    """Render ``obj`` to a file, open it in the browser, return the path.

    Filenames are timestamped so repeated runs never collide and the browser
    can never serve a cached copy of a previous render.
    """
    suffix, body = _as_page(source(obj))

    directory = outdir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}-{time.strftime('%H%M%S')}{suffix}"
    path.write_text(body, encoding="utf-8")

    opened = False
    if open_it and not os.environ.get("QEC_VIZ_NO_OPEN"):
        opened = _launch(path)

    print(f"viz: {path}" if opened else f"viz: wrote {path} (open it manually)")
    return path
