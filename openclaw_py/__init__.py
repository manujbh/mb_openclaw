"""Thin Python wrapper that delegates to the Node.js openclaw CLI."""

import os
import shutil
import subprocess
import sys


def _find_node() -> str:
    node = shutil.which("node")
    if node is None:
        print(
            "Error: Node.js is required but not found on PATH.\n"
            "Install Node >= 22: https://nodejs.org/",
            file=sys.stderr,
        )
        sys.exit(1)
    return node


def _package_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    node = _find_node()
    entry = os.path.join(_package_root(), "openclaw.mjs")

    if not os.path.isfile(entry):
        # Fallback: try npx if installed globally via npm
        npx = shutil.which("npx")
        if npx:
            raise SystemExit(
                subprocess.call([npx, "openclaw"] + sys.argv[1:])
            )
        print(
            "Error: openclaw.mjs not found. Run from the project root or "
            "install via npm: npm install -g openclaw",
            file=sys.stderr,
        )
        sys.exit(1)

    raise SystemExit(subprocess.call([node, entry] + sys.argv[1:]))
