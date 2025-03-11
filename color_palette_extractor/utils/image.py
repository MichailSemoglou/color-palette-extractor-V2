#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image processing utilities for the Color Palette Extractor 2.0
"""

import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)

# List of supported image extensions
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

def is_valid_image(file_path):
    """Check if a file is a valid image.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if the file is a valid image, False otherwise
    """
    if not os.path.isfile(file_path):
        return False
        
    # Check file extension
    if not file_path.lower().endswith(SUPPORTED_EXTENSIONS):
        return False
        
    # Try to open the file as an image
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception as e:
        logger.debug(f"Invalid image file {file_path}: {str(e)}")
        return False

def find_images_in_directory(directory_path, recursive=False):
    """Find all valid image files in a directory.
    
    Args:
        directory_path (str): Path to the directory
        recursive (bool): Whether to search recursively
        
    Returns:
        list: List of paths to valid image files
    """
    if not os.path.isdir(directory_path):
        logger.error(f"Directory does not exist: {directory_path}")
        return []
        
    image_paths = []
    
    if recursive:
        # Walk through directory recursively
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if is_valid_image(file_path):
                    image_paths.append(file_path)
    else:
        # Only search in the top-level directory
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if is_valid_image(file_path):
                image_paths.append(file_path)
                
    logger.info(f"Found {len(image_paths)} valid images in {directory_path}")
    return image_paths

def resize_for_processing(image, max_dimension=1000):
    """Resize an image to a maximum dimension while preserving aspect ratio.
    
    Args:
        image (PIL.Image): PIL Image object
        max_dimension (int): Maximum dimension (width or height)
        
    Returns:
        PIL.Image: Resized image
    """
    width, height = image.size
    if max(width, height) <= max_dimension:
        return image
        
    scale_factor = max_dimension / max(width, height)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    return image.resize((new_width, new_height), Image.LANCZOS)

def ensure_rgb(image):
    """Ensure image is in RGB mode.
    
    Args:
        image (PIL.Image): PIL Image object
        
    Returns:
        PIL.Image: Image in RGB mode
    """
    if image.mode != 'RGB':
        return image.convert('RGB')
    return image
