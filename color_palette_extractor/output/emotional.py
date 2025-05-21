#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Emotional analysis output for the Color Palette Extractor.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def save_emotional_analysis(analysis_results, filename="color_emotions.txt"):
    """Save emotional analysis to a text file.
    
    Args:
        analysis_results (dict): Results from analyze_palette_emotions
        filename (str): Output filename
        
    Returns:
        str: Path to the created text file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write("COLOR PALETTE EMOTIONAL ANALYSIS\n")
            f.write("===============================\n\n")
            
            # Overall analysis
            f.write("OVERALL PALETTE ANALYSIS:\n")
            f.write("-----------------------\n")
            f.write(f"Dominant Emotions: {', '.join(analysis_results['overall']['dominant_emotions'])}\n\n")
            f.write(f"Harmony Analysis: {analysis_results['overall']['harmony_analysis']}\n\n")
            f.write(f"Brand Recommendations: {analysis_results['overall']['brand_recommendations']}\n\n")
            
            # Individual colors
            f.write("INDIVIDUAL COLOR ANALYSIS:\n")
            f.write("------------------------\n")
            for i, color in enumerate(analysis_results['colors']):
                f.write(f"Color {i+1} ({color['hex']}, {color['color_name'].capitalize()}):\n")
                f.write(f"  Emotional Response: {', '.join(color['emotions'])}\n")
                f.write(f"  Associations: {', '.join(color['associations'])}\n")
                f.write(f"  Intensity: {color['intensity'].capitalize()}\n")
                f.write(f"  Brand Fit: {', '.join(color['brand_fit'])}\n\n")
        
        # Also save as JSON for potential future use
        json_filename = os.path.splitext(filename)[0] + ".json"
        with open(json_filename, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        logger.info(f"Saved emotional analysis to {filename} and {json_filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Error saving emotional analysis to {filename}: {str(e)}")
        raise
