#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file output generation for the Color Palette Extractor 2.0
"""

import os
import logging
from ..utils.color import rgb_to_cmyk

logger = logging.getLogger(__name__)

def save_palette_and_harmonies(color_palette, harmonies, filename="color_info.txt"):
    """Save the color palette and harmonies to a text file.
    
    Args:
        color_palette (list): List of color tuples from extract_color_palette
        harmonies (dict): Dictionary of color harmonies from get_harmonies
        filename (str): Output filename
        
    Returns:
        str: Path to the created text file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write("COLOR PALETTE INFORMATION\n")
            f.write("========================\n\n")
            
            f.write("Color Palette:\n")
            f.write("-------------\n")
            for i, color in enumerate(color_palette):
                f.write(f"Color {i+1}:\n")
                f.write(f"  HEX: {color[0]}\n")
                f.write(f"  RGB: {color[1]}\n")
                f.write(f"  CMYK: {color[2]}\n\n")
            
            f.write("\nColor Harmonies:\n")
            f.write("---------------\n")
            for harmony_type, harmony_sets in harmonies.items():
                f.write(f"\n{harmony_type.capitalize()}:\n")
                for i, harmony_set in enumerate(harmony_sets):
                    f.write(f"  Set {i+1} (from Color {i+1}):\n")
                    for color_name, color_hex in harmony_set.items():
                        # Convert hex to RGB and CMYK
                        hex_color = color_hex.lstrip('#')
                        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                        cmyk = rgb_to_cmyk(*rgb)
                        
                        f.write(f"    {color_name}:\n")
                        f.write(f"      HEX: {color_hex}\n")
                        f.write(f"      RGB: {rgb}\n")
                        f.write(f"      CMYK: {cmyk}\n")
                    f.write("\n")
        
        logger.info(f"Saved color information to {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Error saving color information to {filename}: {str(e)}")
        raise
