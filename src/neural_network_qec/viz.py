"""Portable viewer for stim diagrams.

A plain Python script has no display system, so ``print()`` on a stim diagram
falls back to text. This module supplies the missing half: it renders the
diagram to a file and opens it in the system browser.

    from neural_network_qec.viz import show
    show(circuit.diagram("timeline-svg"), name="timeline")

The diagram-viewer path uses only the standard library. If no opener can be
found it prints the path instead of raising -- looking at a diagram must never
be able to fail a script. Threshold plotting uses Matplotlib and NumPy.

Set ``QEC_VIZ_NO_OPEN=1`` to write without opening (CI, or batch renders).
Set ``QEC_VIZ_DIR`` to choose the output directory.

This file also contains threshold-plot helpers.
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

import matplotlib.pyplot as plt
import numpy as np

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


# Plotting the threshold
def threshold_plot(df):

    def find_crossing(df, d_small, d_big):
        """Physical error rate where the d_small and d_big curves cross.

        Between two neighbouring sweep points each curve is treated as a straight
        line on the log-log plot, so the crossing is found by linear interpolation
        of log(p) and log(LER). Returns (p, LER), or None if they never cross.
        """
        a = df[df["distance"] == d_small].sort_values("physical_p")
        b = df[df["distance"] == d_big].sort_values("physical_p")
        p = a["physical_p"].to_numpy()
        with np.errstate(divide="ignore", invalid="ignore"):
            la = np.log(a["LER_per_round"].to_numpy())
            lb = np.log(b["LER_per_round"].to_numpy())
        gap = la - lb  # > 0: the smaller code is worse, < 0: it is better

        for i in range(len(p) - 1):
            if not (np.isfinite(gap[i]) and np.isfinite(gap[i + 1])):
                continue  # a point with 0 errors has no log, skip it
            if gap[i] * gap[i + 1] < 0:  # sign flip = the curves crossed here
                t = gap[i] / (gap[i] - gap[i + 1])
                log_p = np.log(p[i]) + t * (np.log(p[i + 1]) - np.log(p[i]))
                log_y = la[i] + t * (la[i + 1] - la[i])
                return np.exp(log_p), np.exp(log_y)
        return None

    distances = sorted(df["distance"].unique())
    crossings = [
        c
        for c in (
            find_crossing(df, d1, d2)
            for d1, d2 in zip(distances, distances[1:], strict=False)
        )
        if c is not None
    ]

    plt.figure(figsize=(12, 10))

    colors = {3: "#1f77b4", 5: "#2ca02c", 7: "#d62728"}

    for d in sorted(df["distance"].unique()):
        sub_df = df[df["distance"] == d].sort_values("physical_p")

        plt.plot(
            sub_df["physical_p"],
            sub_df["LER_per_round"],
            marker="o",
            linestyle="-",
            color=colors.get(d, "black"),
            label=f"d={d}",
        )

    plt.xscale("log")
    plt.yscale("log")

    if crossings:
        # One number for the threshold: the geometric mean of the pairwise
        # crossings (d=3 vs 5, d=5 vs 7), because the axes are logarithmic.
        p_th = float(np.exp(np.mean([np.log(x) for x, _ in crossings])))
        y_th = float(np.exp(np.mean([np.log(y) for _, y in crossings])))
        y_bottom, y_top = plt.ylim()  # remember the axis range before drawing on it

        # A dashed line from the crossing straight down to the x-axis...
        plt.vlines(
            p_th,
            y_bottom,
            y_th,
            colors="black",
            linestyles="--",
            linewidth=1.2,
            label=f"threshold  p = {p_th:.4f}",
        )
        plt.plot(p_th, y_th, marker="o", color="black", markersize=8, zorder=5)
        plt.ylim(
            y_bottom, y_top
        )  # stop Matplotlib re-scaling, so the line meets the axis
        # ...and its value written on the axis, just under the tick labels.
        plt.annotate(
            f"{p_th:.4f}",
            xy=(p_th, 0),
            xycoords=("data", "axes fraction"),
            xytext=(0, -38),
            textcoords="offset points",
            ha="center",
            fontsize=11,
            fontweight="bold",
            arrowprops=dict(arrowstyle="-", color="black", linestyle="--"),
        )
        print(f"threshold estimate (curves cross): p = {p_th:.5f}")
    else:
        print("no crossing found - widen the sweep range in np.logspace(...)")

    plt.xlabel(r"physical error rate", fontsize=12)
    plt.ylabel(r"LER_per_round", fontsize=12)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(title="distance")

    plt.show()
