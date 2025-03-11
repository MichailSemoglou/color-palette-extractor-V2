#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for the Color Palette Extractor.
"""

import sys
from .cli import main as cli_main

if __name__ == "__main__":
    sys.exit(cli_main())
