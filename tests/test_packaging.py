"""Packaging invariants.

Regression guard for a defect that shipped silently: ``pyproject.toml`` declared
``qec = "neural_network_qec.cli:main"`` while no ``cli`` module existed, so every
install produced a ``qec`` command that died on ImportError. Nothing caught it,
because there was no test suite. If a console script is ever declared again,
``test_declared_console_scripts_are_importable`` fails until it actually resolves.
"""

from importlib.metadata import distribution

import neural_network_qec

DIST = "neural-network-qec"


def test_package_imports() -> None:
    assert neural_network_qec.__version__


def test_declared_console_scripts_are_importable() -> None:
    for ep in distribution(DIST).entry_points:
        if ep.group == "console_scripts":
            ep.load()
