"""Command line entry point.

Wired to the `qec` command via [project.scripts] in pyproject.toml, so after
`uv sync` you can run `qec --shots 100` from anywhere in the project.
"""

import argparse

from neural_network_qec import __version__
from neural_network_qec.decoder import syndrome_weight


def main() -> None:
    parser = argparse.ArgumentParser(prog="qec", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--shots", type=int, default=10, help="number of syndromes to sample"
    )
    args = parser.parse_args()

    for shot in range(args.shots):
        print(f"shot {shot}: weight={syndrome_weight([shot % 2, (shot // 2) % 2])}")


if __name__ == "__main__":
    main()
