"""
Color Palette Extractor

A tool to extract color palettes from images and generate harmonies.
"""

__version__ = "2.1.0"
__author__ = "Michail Semoglou"

import os

# Define paths for resources
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(PACKAGE_DIR, "fonts")

# Define version info
VERSION_INFO = {
    "major": 2,
    "minor": 1,
    "patch": 0,
    "status": "stable",
}

# Make key functions available at package level
from .core import extract_color_palette
from .harmonies import get_harmonies
from .output.pdf import save_palette_to_pdf
from .output.text import save_palette_and_harmonies
from .batch import process_images, process_folder

def get_version_string():
    """Return version string."""
    return __version__
