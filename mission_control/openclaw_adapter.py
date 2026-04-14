"""OpenClaw integration layer.

This module is intentionally small: it shells out to the OpenClaw CLI.
If your OpenClaw binary name differs, change OPENCLAW_BIN.
"""

from __future__ import annotations

import shlex
import subprocess
from typing import Tuple

# If your OpenClaw executable is not called "openclaw", change this.
OPENCLAW_BIN = "openclaw"

def _run_capture(args: str) -> Tuple[int, str, str]:
    """Run OpenClaw with the given args string and capture output."""
    cmd = [OPENCLAW_BIN] + shlex.split(args)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", f"OpenClaw binary not found: {OPENCLAW_BIN!r}. Is it installed and on PATH?\n"
    except Exception as e:
        return 1, "", f"Failed to run OpenClaw: {e}\n"

def openclaw_status() -> Tuple[int, str, str]:
    """Primary command: openclaw status"""
    return _run_capture("status")

def openclaw_run(args: str) -> Tuple[int, str, str]:
    """Run arbitrary OpenClaw args (e.g. "run --task ...")."""
    return _run_capture(args)