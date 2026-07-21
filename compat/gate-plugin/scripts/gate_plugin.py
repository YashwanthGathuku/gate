#!/usr/bin/env python3
"""Deprecated installed-plugin adapter for the canonical TheUstad package."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    print("GATE_DEPRECATED use $theustad:<command>", file=sys.stderr)
    canonical = (
        Path(__file__).resolve().parents[2]
        / "theustad"
        / "scripts"
        / "theustad_plugin.py"
    )
    if not canonical.is_file():
        print(
            f"GATE_PLUGIN_ERROR canonical TheUstad plugin launcher is missing: "
            f"{canonical}",
            file=sys.stderr,
        )
        return 2
    return subprocess.run(
        [os.path.abspath(sys.executable), str(canonical), *sys.argv[1:]],
        shell=False,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
