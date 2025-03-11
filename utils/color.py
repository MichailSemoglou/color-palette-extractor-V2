#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Color conversion utilities for the Color Palette Extractor 2.0
"""

def rgb_to_cmyk(r, g, b):
    """Convert RGB to CMYK color space.
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
    
    Returns:
        tuple: CMYK values (c, m, y, k) as percentages (0-100)
    """
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100

    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    
    if k == 1:  # Pure black
        return 0, 0, 0, 100
    
    c = (c - k) / (1 - k) * 100
    m = (m - k) / (1 - k) * 100
    y = (y - k) / (1 - k) * 100
    k = k * 100
    
    return round(c), round(m), round(y), round(k)

def cmyk_to_rgb(c, m, y, k):
    """Convert CMYK to RGB color space.
    
    Args:
        c (float): Cyan component (0-100)
        m (float): Magenta component (0-100)
        y (float): Yellow component (0-100)
        k (float): Key/Black component (0-100)
    
    Returns:
        tuple: RGB values (r, g, b) as integers (0-255)
    """
    c, m, y, k = c/100.0, m/100.0, y/100.0, k/100.0
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return round(r), round(g), round(b)

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple.
    
    Args:
        hex_color (str): Hex color string (#RRGGBB)
    
    Returns:
        tuple: RGB values (r, g, b) as integers (0-255)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string.
    
    Args:
        rgb (tuple): RGB color tuple (r, g, b) with values 0-255
    
    Returns:
        str: Hex color string (#RRGGBB)
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_contrast_color(hex_color):
    """Determine the best contrasting color (black or white) for text on given background.
    
    Args:
        hex_color (str): Hex color string (#RRGGBB)
    
    Returns:
        str: '#FFFFFF' for white or '#000000' for black
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Calculate luminance - modern formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    return '#000000' if luminance > 0.5 else '#FFFFFF'
