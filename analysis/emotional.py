#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Emotional and psychological color analysis for Color Palette Extractor.
"""

import colorsys
import math
import logging

logger = logging.getLogger(__name__)

# Color psychology database - emotional associations
COLOR_EMOTIONS = {
    # Red range (0-30 degrees or 330-360 degrees in HSV)
    "red": {
        "emotions": ["passionate", "energetic", "exciting", "powerful", "bold"],
        "associations": ["love", "urgency", "attention", "danger", "importance"],
        "brand_fit": ["food", "entertainment", "sports", "emergency services"]
    },
    # Orange range (30-60 degrees in HSV)
    "orange": {
        "emotions": ["enthusiastic", "playful", "cheerful", "confident", "friendly"],
        "associations": ["creativity", "youth", "affordability", "energy"],
        "brand_fit": ["food", "children's products", "budget brands", "fitness"]
    },
    # Yellow range (60-90 degrees in HSV)
    "yellow": {
        "emotions": ["optimistic", "happy", "warm", "alert", "stimulating"],
        "associations": ["sunshine", "joy", "caution", "intellect"],
        "brand_fit": ["leisure", "food", "warning signs", "education"]
    },
    # Green range (90-150 degrees in HSV)
    "green": {
        "emotions": ["peaceful", "growth-oriented", "balanced", "fresh", "natural"],
        "associations": ["nature", "wealth", "health", "renewal", "safety"],
        "brand_fit": ["environment", "finance", "healthcare", "organic products"]
    },
    # Teal/Cyan range (150-195 degrees in HSV)
    "teal": {
        "emotions": ["calming", "refreshing", "modern", "clarity", "cleanliness"],
        "associations": ["water", "technology", "cleanliness", "logic"],
        "brand_fit": ["technology", "healthcare", "cleaning products", "water brands"]
    },
    # Blue range (195-240 degrees in HSV)
    "blue": {
        "emotions": ["trustworthy", "reliable", "calm", "secure", "professional"],
        "associations": ["stability", "trust", "wisdom", "loyalty", "tranquility"],
        "brand_fit": ["finance", "technology", "healthcare", "corporate"]
    },
    # Purple range (240-270 degrees in HSV)
    "purple": {
        "emotions": ["creative", "royal", "mysterious", "spiritual", "luxurious"],
        "associations": ["luxury", "creativity", "wisdom", "mystery", "quality"],
        "brand_fit": ["luxury goods", "creative services", "spirituality", "anti-aging"]
    },
    # Pink range (270-330 degrees in HSV)
    "pink": {
        "emotions": ["romantic", "feminine", "playful", "compassionate", "nurturing"],
        "associations": ["love", "femininity", "youth", "sweetness", "compassion"],
        "brand_fit": ["beauty", "children's products", "confectionery", "feminine products"]
    },
    # Neutral colors
    "brown": {
        "emotions": ["reliable", "sturdy", "warm", "natural", "grounded"],
        "associations": ["earth", "wood", "outdoors", "reliability", "comfort"],
        "brand_fit": ["coffee", "chocolate", "craftsmanship", "outdoors", "furniture"]
    },
    "gray": {
        "emotions": ["neutral", "balanced", "professional", "sophisticated", "timeless"],
        "associations": ["formality", "neutrality", "subtlety", "professionalism"],
        "brand_fit": ["business", "technology", "luxury", "minimal designs"]
    },
    "black": {
        "emotions": ["powerful", "sophisticated", "elegant", "mysterious", "authoritative"],
        "associations": ["luxury", "power", "elegance", "formality", "sophistication"],
        "brand_fit": ["luxury brands", "high-end products", "technology", "formal services"]
    },
    "white": {
        "emotions": ["pure", "clean", "simple", "innocent", "peaceful"],
        "associations": ["simplicity", "cleanliness", "purity", "minimalism", "clarity"],
        "brand_fit": ["healthcare", "technology", "weddings", "minimalist brands"]
    }
}

# Harmony psychology effects
HARMONY_EFFECTS = {
    "complementary": "Creates a vibrant, high-contrast palette. Ideal for brands wanting to stand out or create energy. Can be visually striking and commanding of attention.",
    "analogous": "Creates a harmonious, cohesive palette with low tension. Great for creating a unified, professional look that feels comfortable and coordinated.",
    "triadic": "Offers visual vibrancy while maintaining balance. Good for creative and playful brands that still want a sense of harmony and completeness.",
    "tetradic": "Provides a rich, varied palette with multiple accent possibilities. Best for brands with diverse product lines or who need a complex visual language.",
    "monochromatic": "Creates a sophisticated, cohesive palette. Excellent for luxury brands, minimalist designs, or when you want the content to be the focus rather than the colors."
}

def identify_color_name(hsv):
    """Identify color name based on HSV values.
    
    Args:
        hsv (tuple): HSV color values (h, s, v) with h in range 0-1
        
    Returns:
        str: Color name
    """
    h, s, v = hsv
    
    # Convert h to degrees (0-360)
    h_deg = h * 360
    
    # Handle grayscale colors first
    if s < 0.15:
        if v < 0.25:
            return "black"
        elif v > 0.85:
            return "white"
        else:
            return "gray"
            
    # Handle brown specially (low saturation reds/oranges/yellows)
    if (h_deg < 50 or h_deg > 330) and s < 0.4 and v < 0.7:
        return "brown"
    
    # Determine hue-based color name
    if h_deg < 30 or h_deg >= 330:
        return "red"
    elif h_deg < 60:
        return "orange"
    elif h_deg < 90:
        return "yellow"
    elif h_deg < 150:
        return "green"
    elif h_deg < 195:
        return "teal"
    elif h_deg < 240:
        return "blue"
    elif h_deg < 270:
        return "purple"
    elif h_deg < 330:
        return "pink"
    
    # Default fallback
    return "gray"

def analyze_palette_emotions(color_palette):
    """Analyze the emotional impact of a color palette.
    
    Args:
        color_palette (list): List of color tuples from extract_color_palette
        
    Returns:
        dict: Emotional analysis results
    """
    results = {
        "colors": [],
        "overall": {
            "dominant_emotions": [],
            "harmony_analysis": "",
            "brand_recommendations": ""
        }
    }
    
    emotion_counts = {}
    color_names = []
    
    # Analyze individual colors
    for i, color in enumerate(color_palette):
        hex_color, rgb, cmyk = color
        
        # Convert RGB to HSV
        r, g, b = [val/255 for val in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # Identify color name
        color_name = identify_color_name((h, s, v))
        color_names.append(color_name)
        
        # Get emotional associations
        emotions = COLOR_EMOTIONS.get(color_name, {}).get("emotions", [])
        associations = COLOR_EMOTIONS.get(color_name, {}).get("associations", [])
        brand_fit = COLOR_EMOTIONS.get(color_name, {}).get("brand_fit", [])
        
        # Add to results
        color_result = {
            "hex": hex_color,
            "color_name": color_name,
            "emotions": emotions,
            "associations": associations,
            "brand_fit": brand_fit,
            "intensity": "strong" if s > 0.7 and v > 0.7 else "moderate" if s > 0.4 else "subtle"
        }
        results["colors"].append(color_result)
        
        # Count emotions for overall analysis
        for emotion in emotions:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1
    
    # Determine dominant emotions
    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
    results["overall"]["dominant_emotions"] = [emotion for emotion, count in sorted_emotions[:3]]
    
    # Analyze color distribution
    color_name_counts = {}
    for name in color_names:
        if name in color_name_counts:
            color_name_counts[name] += 1
        else:
            color_name_counts[name] = 1
    
    color_diversity = len(color_name_counts)
    
    # Analyze harmony
    has_complementary = len(set(["red", "green"]).intersection(set(color_names))) == 2 or \
                       len(set(["blue", "orange"]).intersection(set(color_names))) == 2 or \
                       len(set(["yellow", "purple"]).intersection(set(color_names))) == 2
                       
    has_analogous = any(
        sum(1 for name in color_names if name in group) >= 3
        for group in [
            ["red", "orange", "yellow"],
            ["yellow", "green", "teal"],
            ["teal", "blue", "purple"],
            ["purple", "pink", "red"]
        ]
    )
    
    dominant_harmony = None
    if len(color_name_counts) == 1 or (len(color_name_counts) == 2 and "white" in color_name_counts):
        dominant_harmony = "monochromatic"
    elif has_complementary and not has_analogous:
        dominant_harmony = "complementary"
    elif has_analogous and not has_complementary:
        dominant_harmony = "analogous"
    elif color_diversity >= 4:
        dominant_harmony = "tetradic"
    elif color_diversity == 3:
        dominant_harmony = "triadic"
    else:
        # Default if we can't determine
        dominant_harmony = "mixed"
    
    # Add harmony analysis
    if dominant_harmony in HARMONY_EFFECTS:
        results["overall"]["harmony_analysis"] = HARMONY_EFFECTS[dominant_harmony]
    else:
        results["overall"]["harmony_analysis"] = "Mixed color harmony providing a balanced visual effect."
    
    # Generate brand recommendations
    primary_colors = [name for name, count in sorted(color_name_counts.items(), key=lambda x: x[1], reverse=True)]
    
    if not primary_colors:
        results["overall"]["brand_recommendations"] = "Unable to determine brand recommendations."
    else:
        primary_color = primary_colors[0]
        
        industry_fits = []
        for color in primary_colors[:2]:  # Use top two colors
            if color in COLOR_EMOTIONS:
                industry_fits.extend(COLOR_EMOTIONS[color]["brand_fit"])
        
        top_industries = list(set(industry_fits))[:3]  # Get unique industries, limit to top 3
        
        emotion_str = ", ".join(results["overall"]["dominant_emotions"])
        industry_str = ", ".join(top_industries) if top_industries else "various industries"
        
        recommendations = f"This color palette evokes feelings of {emotion_str}. "
        recommendations += f"It would be well-suited for brands in {industry_str}. "
        
        if dominant_harmony:
            recommendations += f"The {dominant_harmony} color relationship creates {HARMONY_EFFECTS.get(dominant_harmony, 'a balanced visual effect')}. "
        
        results["overall"]["brand_recommendations"] = recommendations
    
    return results
