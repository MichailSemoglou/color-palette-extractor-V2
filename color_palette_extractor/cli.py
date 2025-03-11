#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command line interface for the Color Palette Extractor.
"""

import os
import sys
import argparse
import logging
import time
from datetime import datetime

from color_palette_extractor import __version__
from color_palette_extractor.core import extract_color_palette
from color_palette_extractor.harmonies import get_harmonies
from color_palette_extractor.output.pdf import save_palette_to_pdf
from color_palette_extractor.output.text import save_palette_and_harmonies
from color_palette_extractor.batch import process_images, process_folder
from color_palette_extractor.utils.image import is_valid_image, find_images_in_directory
from color_palette_extractor.utils.cache import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("color_extractor")

def configure_logging(log_level, log_file=None):
    """Configure logging level and output file.
    
    Args:
        log_level (str): Logging level (debug, info, warning, error)
        log_file (str, optional): Path to log file
    """
    # Set log level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        root_logger.addHandler(file_handler)

def parse_arguments():
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=f"Color Palette Extractor v{__version__}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i", "--image",
        help="Path to a single image file"
    )
    input_group.add_argument(
        "-d", "--directory",
        help="Path to a directory of images"
    )
    input_group.add_argument(
        "-f", "--file-list",
        help="Path to a text file containing image paths (one per line)"
    )
    
    # Output options
    parser.add_argument(
        "-o", "--output-dir",
        help="Directory to save results (default: same as input)"
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Generate only PDF reports (no text files)"
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="Generate only text files (no PDF reports)"
    )
    
    # Processing options
    parser.add_argument(
        "-n", "--num-colors",
        type=int,
        default=6,
        help="Number of colors to extract (1-12)"
    )
    parser.add_argument(
        "-j", "--jobs",
        type=int,
        default=None,
        help="Number of parallel jobs (default: number of CPU cores)"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process directories recursively"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching of results"
    )
    
    # Logging options
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="Set logging level"
    )
    parser.add_argument(
        "--log-file",
        help="Save log to file"
    )
    
    # Version info
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"Color Palette Extractor v{__version__}"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.num_colors < 1 or args.num_colors > 12:
        parser.error("Number of colors must be between 1 and 12")
    
    if args.pdf_only and args.text_only:
        parser.error("Cannot use both --pdf-only and --text-only")
    
    return args

def main():
    """Main entry point for the command line interface."""
    args = parse_arguments()
    
    # Configure logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.log_file:
        log_file = args.log_file
    else:
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"color_extractor_{timestamp}.log")
    
    configure_logging(args.log_level, log_file)
    
    logger.info(f"Color Palette Extractor v{__version__}")
    start_time = time.time()
    
    # Determine output formats
    generate_pdf = not args.text_only
    generate_text = not args.pdf_only
    
    # Process based on input type
    try:
        if args.image:
            # Single image mode
            image_path = os.path.abspath(args.image)
            logger.info(f"Processing single image: {image_path}")
            
            if not os.path.isfile(image_path):
                logger.error(f"File not found: {image_path}")
                return 1
                
            if not is_valid_image(image_path):
                logger.error(f"Not a valid image file: {image_path}")
                return 1
            
            # Create cache manager if enabled
            cache_manager = None if args.no_cache else CacheManager()
            
            # Process the image
            result = process_images(
                [image_path],
                num_colors=args.num_colors,
                output_dir=args.output_dir,
                generate_pdf=generate_pdf,
                generate_text=generate_text,
                use_cache=not args.no_cache,
                max_workers=1  # No parallelism for single image
            )
            
            if result['successful'] == 0:
                logger.error(f"Failed to process image: {result['results'][0].get('error', 'Unknown error')}")
                return 1
            
            logger.info(f"Successfully processed image in {result['processing_time']:.2f} seconds")
            logger.info(f"Output files: {result['results'][0]['output_files']}")
            
        elif args.directory:
            # Directory mode
            dir_path = os.path.abspath(args.directory)
            logger.info(f"Processing directory: {dir_path} (recursive: {args.recursive})")
            
            if not os.path.isdir(dir_path):
                logger.error(f"Directory not found: {dir_path}")
                return 1
            
            # Process the directory
            result = process_folder(
                dir_path,
                num_colors=args.num_colors,
                output_dir=args.output_dir,
                recursive=args.recursive,
                generate_pdf=generate_pdf,
                generate_text=generate_text,
                use_cache=not args.no_cache,
                max_workers=args.jobs
            )
            
            if result['total'] == 0:
                logger.warning("No valid images found in directory")
                return 0
            
            logger.info(f"Processed {result['total']} images in {result['processing_time']:.2f} seconds")
            logger.info(f"Successful: {result['successful']}, Failed: {result['failed']}")
            
            if result['failed'] > 0:
                return 1
            
        elif args.file_list:
            # File list mode
            list_path = os.path.abspath(args.file_list)
            logger.info(f"Processing images from list: {list_path}")
            
            if not os.path.isfile(list_path):
                logger.error(f"File list not found: {list_path}")
                return 1
            
            # Read image paths from file
            with open(list_path, 'r') as f:
                image_paths = [line.strip() for line in f if line.strip()]
            
            if not image_paths:
                logger.warning("No image paths found in file list")
                return 0
            
            logger.info(f"Found {len(image_paths)} image paths in list")
            
            # Process the images
            result = process_images(
                image_paths,
                num_colors=args.num_colors,
                output_dir=args.output_dir,
                generate_pdf=generate_pdf,
                generate_text=generate_text,
                use_cache=not args.no_cache,
                max_workers=args.jobs
            )
            
            logger.info(f"Processed {result['total']} images in {result['processing_time']:.2f} seconds")
            logger.info(f"Successful: {result['successful']}, Failed: {result['failed']}")
            
            if result['failed'] > 0:
                return 1
        
        total_time = time.time() - start_time
        logger.info(f"Total execution time: {total_time:.2f} seconds")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        logger.debug("Exception details:", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
