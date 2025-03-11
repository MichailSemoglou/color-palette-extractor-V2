#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Color harmony generation functionality for the Color Palette Extractor.
"""

import colorsys
import logging

logger = logging.getLogger(__name__)

def rgb_to_hex(rgb):
    """Convert RGB tuple to HEX string.
    
    Args:
        rgb (tuple): RGB color tuple (r, g, b)
        
    Returns:
        str: Hex color string (#RRGGBB)
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def is_dark(hex_color):
    """Determine if a color is dark based on its luminance.
    
    Args:
        hex_color (str): Hex color string (#RRGGBB)
        
    Returns:
        bool: True if color is dark, False otherwise
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.5

def get_harmonies(color_palette, harmony_types=None):
    """Generate common color harmonies based on the palette.
    
    Args:
        color_palette (list): List of color tuples from extract_color_palette
        harmony_types (list, optional): List of harmony types to generate
            Valid types: "complementary", "analogous", "triadic", "tetradic", "tints", "shades"
            If None, all harmony types will be generated
    
    Returns:
        dict: Dictionary of color harmonies
    """
    all_harmony_types = ["complementary", "analogous", "triadic", "tetradic", "tints", "shades"]
    
    # If harmony_types is None, use all types
    harmony_types = harmony_types or all_harmony_types
    
    # Initialize harmonies dictionary
    harmonies = {harmony_type: [] for harmony_type in harmony_types}
    
    logger.debug(f"Generating {len(harmony_types)} harmony types for {len(color_palette)} colors")
    
    for color in color_palette:
        rgb = color[1]
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

        # Complementary
        if "complementary" in harmony_types:
            comp_h = (h + 0.5) % 1
            comp_rgb = colorsys.hsv_to_rgb(comp_h, s, v)
            harmonies["complementary"].append({
                "Base": rgb_to_hex(rgb),
                "Complement": rgb_to_hex(tuple(int(x*255) for x in comp_rgb))
            })

        # Analogous
        if "analogous" in harmony_types:
            analog_h1 = (h + 1/12) % 1
            analog_h2 = (h - 1/12) % 1
            analog_rgb1 = colorsys.hsv_to_rgb(analog_h1, s, v)
            analog_rgb2 = colorsys.hsv_to_rgb(analog_h2, s, v)
            harmonies["analogous"].append({
                "Base": rgb_to_hex(rgb),
                "Analog 1": rgb_to_hex(tuple(int(x*255) for x in analog_rgb1)),
                "Analog 2": rgb_to_hex(tuple(int(x*255) for x in analog_rgb2))
            })

        # Triadic
        if "triadic" in harmony_types:
            triad_h1 = (h + 1/3) % 1
            triad_h2 = (h + 2/3) % 1
            triad_rgb1 = colorsys.hsv_to_rgb(triad_h1, s, v)
            triad_rgb2 = colorsys.hsv_to_rgb(triad_h2, s, v)
            harmonies["triadic"].append({
                "Base": rgb_to_hex(rgb),
                "Triad 1": rgb_to_hex(tuple(int(x*255) for x in triad_rgb1)),
                "Triad 2": rgb_to_hex(tuple(int(x*255) for x in triad_rgb2))
            })

        # Tetradic
        if "tetradic" in harmony_types:
            tetra_h1 = (h + 0.25) % 1
            tetra_h2 = (h + 0.5) % 1
            tetra_h3 = (h + 0.75) % 1
            tetra_rgb1 = colorsys.hsv_to_rgb(tetra_h1, s, v)
            tetra_rgb2 = colorsys.hsv_to_rgb(tetra_h2, s, v)
            tetra_rgb3 = colorsys.hsv_to_rgb(tetra_h3, s, v)
            harmonies["tetradic"].append({
                "Base": rgb_to_hex(rgb),
                "Tetra 1": rgb_to_hex(tuple(int(x*255) for x in tetra_rgb1)),
                "Tetra 2": rgb_to_hex(tuple(int(x*255) for x in tetra_rgb2)),
                "Tetra 3": rgb_to_hex(tuple(int(x*255) for x in tetra_rgb3))
            })

        # Tints
        if "tints" in harmony_types:
            tints = []
            for i in range(5):
                tint_s = max(0, s - (s * (i / 4)))
                tint_v = min(1, v + ((1 - v) * (i / 4)))
                tint_rgb = colorsys.hsv_to_rgb(h, tint_s, tint_v)
                tints.append(rgb_to_hex(tuple(int(x*255) for x in tint_rgb)))
            harmonies["tints"].append({f"Tint {i+1}": tint for i, tint in enumerate(tints)})

        # Shades
        if "shades" in harmony_types:
            shades = []
            for i in range(5):
                shade_v = v * (1 - i / 4)
                shade_rgb = colorsys.hsv_to_rgb(h, s, shade_v)
                shades.append(rgb_to_hex(tuple(int(x*255) for x in shade_rgb)))
            harmonies["shades"].append({f"Shade {i+1}": shade for i, shade in enumerate(shades)})

    return harmonies
