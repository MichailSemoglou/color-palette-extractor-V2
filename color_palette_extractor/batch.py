#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch processing functionality for the Color Palette Extractor.
"""

import os
import time
import logging
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

from .core import extract_color_palette
from .harmonies import get_harmonies
from color_palette_extractor.output.pdf import save_palette_to_pdf
from color_palette_extractor.output.text import save_palette_and_harmonies
from color_palette_extractor.utils.image import find_images_in_directory, is_valid_image
from color_palette_extractor.utils.cache import CacheManager

logger = logging.getLogger(__name__)

def process_single_image(image_path, num_colors=6, output_dir=None, 
                        generate_pdf=True, generate_text=True, 
                        cache_manager=None, config=None):
    """Process a single image to extract color palette and harmonies.
    
    Args:
        image_path (str): Path to the image file
        num_colors (int): Number of colors to extract
        output_dir (str, optional): Directory to save output files
            If None, output files will be saved in the same directory as the image
        generate_pdf (bool): Whether to generate a PDF report
        generate_text (bool): Whether to generate a text file
        cache_manager (CacheManager, optional): Cache manager instance
        config (dict, optional): Configuration options
            
    Returns:
        dict: Processing result with keys:
            - image_path: Path to the processed image
            - success: True if processing was successful, False otherwise
            - error: Error message if processing failed
            - output_files: List of output file paths
            - processing_time: Processing time in seconds
    """
    start_time = time.time()
    output_files = []
    
    try:
        # Validate input file
        if not os.path.isfile(image_path):
            return {
                'image_path': image_path,
                'success': False,
                'error': f"File not found: {image_path}",
                'output_files': [],
                'processing_time': time.time() - start_time
            }
            
        if not is_valid_image(image_path):
            return {
                'image_path': image_path,
                'success': False,
                'error': f"Not a valid image file: {image_path}",
                'output_files': [],
                'processing_time': time.time() - start_time
            }
        
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(image_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filenames
        basename = os.path.splitext(os.path.basename(image_path))[0]
        pdf_path = os.path.join(output_dir, f"{basename}_palette.pdf")
        text_path = os.path.join(output_dir, f"{basename}_info.txt")
        
        # Check cache for palette
        palette = None
        if cache_manager is not None:
            palette = cache_manager.get_cached_result(image_path, num_colors)
        
        # Extract palette if not in cache
        if palette is None:
            palette = extract_color_palette(image_path, num_colors)
            
            # Store in cache if cache manager is available
            if cache_manager is not None:
                cache_manager.store_result(image_path, num_colors, palette)
        
        # Generate harmonies
        harmonies = get_harmonies(palette)
        
        # Generate emotional analysis if requested
        emotional_analysis = None
        if config and config.get('emotional_analysis'):
            try:
                from color_palette_extractor.analysis.emotional import analyze_palette_emotions
                from color_palette_extractor.output.emotional import save_emotional_analysis
                
                logger.debug(f"Generating emotional analysis for {image_path}")
                emotional_analysis = analyze_palette_emotions(palette)
                
                if generate_text:
                    emotional_filename = os.path.join(output_dir, f"{basename}_emotions.txt")
                    save_emotional_analysis(emotional_analysis, emotional_filename)
                    output_files.append(emotional_filename)
                    logger.debug(f"Saved emotional analysis to {emotional_filename}")
            except Exception as e:
                logger.error(f"Error generating emotional analysis for {image_path}: {str(e)}")
                logger.debug(traceback.format_exc())
                emotional_analysis = None
        
        # Save outputs
        if generate_text:
            save_palette_and_harmonies(palette, harmonies, filename=text_path)
            output_files.append(text_path)
        
        if generate_pdf:
            save_palette_to_pdf(
                palette, 
                harmonies, 
                filename=pdf_path, 
                image_filename=image_path,
                emotional_analysis=emotional_analysis,
                config=config
            )
            output_files.append(pdf_path)
        
        processing_time = time.time() - start_time
        logger.info(f"Processed {image_path} in {processing_time:.2f} seconds")
        
        return {
            'image_path': image_path,
            'success': True,
            'output_files': output_files,
            'processing_time': processing_time
        }
        
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")
        logger.debug(traceback.format_exc())
        
        return {
            'image_path': image_path,
            'success': False,
            'error': str(e),
            'output_files': output_files,
            'processing_time': time.time() - start_time
        }

def process_images(image_paths, num_colors=6, output_dir=None, 
                 generate_pdf=True, generate_text=True, 
                 use_cache=True, max_workers=None, config=None):
    """Process multiple images in parallel.
    
    Args:
        image_paths (list): List of image file paths
        num_colors (int): Number of colors to extract
        output_dir (str, optional): Directory to save output files
        generate_pdf (bool): Whether to generate PDF reports
        generate_text (bool): Whether to generate text files
        use_cache (bool): Whether to use caching
        max_workers (int, optional): Maximum number of worker processes
        config (dict, optional): Configuration options
            
    Returns:
        dict: Processing results summary with keys:
            - total: Total number of images
            - successful: Number of successfully processed images
            - failed: Number of failed images
            - processing_time: Total processing time in seconds
            - results: List of individual image processing results
    """
    start_time = time.time()
    
    # Create cache manager if caching is enabled
    cache_manager = CacheManager() if use_cache else None
    
    # Create output directory if specified
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
    
    # Filter out invalid image paths
    valid_paths = [path for path in image_paths if os.path.isfile(path)]
    if len(valid_paths) < len(image_paths):
        logger.warning(f"Skipping {len(image_paths) - len(valid_paths)} invalid file paths")
    
    total_images = len(valid_paths)
    results = []
    
    logger.info(f"Processing {total_images} images with {max_workers or 'auto'} workers")
    
    # If emotional analysis is enabled, log it
    if config and config.get('emotional_analysis'):
        logger.info("Emotional analysis is enabled")
    
    # Process images in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all jobs
        future_to_path = {
            executor.submit(
                process_single_image, 
                path, 
                num_colors, 
                output_dir, 
                generate_pdf, 
                generate_text, 
                cache_manager,
                config
            ): path for path in valid_paths
        }
        
        # Process results as they complete with progress bar
        for future in tqdm(as_completed(future_to_path), total=total_images, desc="Processing images"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                path = future_to_path[future]
                logger.error(f"Unhandled exception processing {path}: {str(e)}")
                logger.debug(traceback.format_exc())
                
                results.append({
                    'image_path': path,
                    'success': False,
                    'error': str(e),
                    'output_files': [],
                    'processing_time': 0
                })
    
    # Calculate summary statistics
    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])
    total_time = time.time() - start_time
    
    logger.info(f"Processed {total_images} images in {total_time:.2f} seconds")
    logger.info(f"Successful: {successful}, Failed: {failed}")
    
    if failed > 0:
        logger.warning("Failed images:")
        for result in results:
            if not result['success']:
                logger.warning(f"  {result['image_path']}: {result.get('error', 'Unknown error')}")
    
    return {
        'total': total_images,
        'successful': successful,
        'failed': failed,
        'processing_time': total_time,
        'results': results
    }

def process_folder(folder_path, num_colors=6, output_dir=None, 
                  recursive=False, **kwargs):
    """Process all images in a folder.
    
    Args:
        folder_path (str): Path to the folder containing images
        num_colors (int): Number of colors to extract
        output_dir (str, optional): Directory to save output files
            If None, output files will be saved in a subdirectory of the input folder
        recursive (bool): Whether to search for images recursively
        **kwargs: Additional arguments to pass to process_images
            
    Returns:
        dict: Processing results (same as process_images)
    """
    if not os.path.isdir(folder_path):
        logger.error(f"Directory not found: {folder_path}")
        return {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'processing_time': 0,
            'results': []
        }
    
    # Set default output directory if not specified
    if output_dir is None:
        output_dir = os.path.join(folder_path, "palette_output")
    
    # Find images in the folder
    image_paths = find_images_in_directory(folder_path, recursive=recursive)
    
    if not image_paths:
        logger.warning(f"No valid images found in {folder_path}")
        return {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'processing_time': 0,
            'results': []
        }
    
    # Process the images
    return process_images(image_paths, num_colors, output_dir, **kwargs)
