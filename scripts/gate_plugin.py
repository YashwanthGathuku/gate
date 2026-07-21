#!/usr/bin/env python3
"""Deprecated Gate plugin launcher forwarding to TheUstad."""

import sys
from pathlib import Path

# Direct execution places scripts/ rather than the repository root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.theustad_plugin import *  # noqa: F401,F403
from scripts.theustad_plugin import main as _main


def main(argv=None):
    print("GATE_DEPRECATED use scripts/theustad_plugin.py", file=sys.stderr)
    return _main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
