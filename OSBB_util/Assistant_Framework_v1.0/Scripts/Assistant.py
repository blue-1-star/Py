#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""OSBB Utility Assistant v1.0."""

from __future__ import annotations

import sys
from pathlib import Path

from osbb_assistant.cli import main


if __name__ == "__main__":
    raise SystemExit(main(script_path=Path(__file__).resolve(), argv=sys.argv[1:]))
