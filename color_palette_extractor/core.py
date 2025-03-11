#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core functionality for extracting color palettes from images.
"""

import numpy as np
from sklearn.cluster import KMeans
from PIL import Image as PILImage
import logging

from color_palette_extractor.utils.color import rgb_to_cmyk

logger = logging.getLogger(__name__)

def extract_color_palette(image_path, num_colors=6, max_dimension=1000):
    """Extract a color palette from an image using KMeans clustering.
    
    Args:
        image_path (str): Path to the image file
        num_colors (int): Number of colors to extract (1-12)
        max_dimension (int): Maximum dimension for image processing
        
    Returns:
        list: List of tuples (hex_color, rgb_color, cmyk_color)
    """
    num_colors = min(num_colors, 12)  # Limit to a maximum of 12 colors
    
    try:
        img = PILImage.open(image_path)
        
        # Calculate new dimensions
        width, height = img.size
        if max(width, height) > max_dimension:
            scale_factor = max_dimension / max(width, height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height), PILImage.LANCZOS)
        
        # Convert image to RGB mode if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)

        # Reshape to a list of pixels
        img_pixels = img_array.reshape((-1, 3))

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
        kmeans.fit(img_pixels)

        # Get the cluster centers (dominant colors)
        dominant_colors = kmeans.cluster_centers_.astype(int)

        # Convert to desired formats
        color_palette = []
        for color in dominant_colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            rgb_color = tuple(color)
            cmyk_color = rgb_to_cmyk(*color)
            color_palette.append((hex_color, rgb_color, cmyk_color))
            
        logger.debug(f"Extracted {len(color_palette)} colors from {image_path}")
        return color_palette
        
    except Exception as e:
        logger.error(f"Error extracting colors from {image_path}: {str(e)}")
        raise
