#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced emotional and psychological color analysis for Color Palette Extractor.
Designed specifically for design students and professionals.
"""

import colorsys
import math
import logging

logger = logging.getLogger(__name__)

# Expanded color psychology database with design-appropriate terms
COLOR_EMOTIONS = {
    # Reds
    "red": {
        "emotions": ["passionate", "energetic", "exciting", "powerful", "bold"],
        "associations": ["love", "urgency", "attention", "danger", "importance"],
        "brand_fit": ["food", "entertainment", "sports", "emergency services"]
    },
    "burgundy": {
        "emotions": ["sophisticated", "rich", "mature", "elegant", "refined"],
        "associations": ["wine", "luxury", "tradition", "warmth", "depth"],
        "brand_fit": ["luxury brands", "wine & spirits", "upscale dining", "heritage brands"]
    },
    "crimson": {
        "emotions": ["dynamic", "bold", "intense", "passionate", "dramatic"],
        "associations": ["strength", "power", "determination", "desire"],
        "brand_fit": ["fashion", "cosmetics", "performance brands", "luxury"]
    },
    
    # Oranges
    "orange": {
        "emotions": ["enthusiastic", "playful", "cheerful", "confident", "friendly"],
        "associations": ["creativity", "youth", "affordability", "energy"],
        "brand_fit": ["food", "children's products", "budget brands", "fitness"]
    },
    "terracotta": {
        "emotions": ["earthy", "warm", "natural", "rustic", "grounded"],
        "associations": ["earth", "pottery", "natural", "outdoors", "warmth"],
        "brand_fit": ["home decor", "natural products", "outdoor brands", "artisanal goods"]
    },
    "coral": {
        "emotions": ["lively", "nurturing", "fresh", "playful", "tropical"],
        "associations": ["ocean", "warmth", "vitality", "tropics"],
        "brand_fit": ["beach wear", "tropical products", "cosmetics", "wellness"]
    },
    
    # Yellows
    "yellow": {
        "emotions": ["optimistic", "happy", "warm", "alert", "stimulating"],
        "associations": ["sunshine", "joy", "caution", "intellect"],
        "brand_fit": ["leisure", "food", "warning signs", "education"]
    },
    "gold": {
        "emotions": ["prestigious", "luxurious", "successful", "traditional", "valuable"],
        "associations": ["wealth", "luxury", "success", "quality", "tradition"],
        "brand_fit": ["luxury brands", "financial services", "premium products", "awards"]
    },
    "mustard": {
        "emotions": ["earthy", "warming", "complex", "spicy", "distinctive"],
        "associations": ["autumn", "spice", "warmth", "coziness"],
        "brand_fit": ["autumn fashion", "craft brands", "artisanal food", "home decor"]
    },
    
    # Greens
    "green": {
        "emotions": ["peaceful", "growth-oriented", "balanced", "fresh", "natural"],
        "associations": ["nature", "wealth", "health", "renewal", "safety"],
        "brand_fit": ["environment", "finance", "healthcare", "organic products"]
    },
    "sage": {
        "emotions": ["calming", "natural", "botanical", "subtle", "sophisticated"],
        "associations": ["plants", "neutrality", "understated elegance", "nature"],
        "brand_fit": ["wellness", "spa", "natural products", "eco-friendly brands"]
    },
    "mint": {
        "emotions": ["fresh", "clean", "revitalizing", "cool", "youthful"],
        "associations": ["freshness", "cleanliness", "coolness", "new beginnings"],
        "brand_fit": ["healthcare", "breath products", "skincare", "modern tech"]
    },
    "olive": {
        "emotions": ["earthy", "natural", "rustic", "traditional", "sophisticated"],
        "associations": ["nature", "durability", "tradition", "peace"],
        "brand_fit": ["outdoor wear", "military-inspired", "eco-friendly", "culinary"]
    },
    
    # Blues
    "teal": {
        "emotions": ["calming", "refreshing", "modern", "clarity", "cleanliness"],
        "associations": ["water", "technology", "cleanliness", "logic"],
        "brand_fit": ["technology", "healthcare", "cleaning products", "water brands"]
    },
    "blue": {
        "emotions": ["trustworthy", "reliable", "calm", "secure", "professional"],
        "associations": ["stability", "trust", "wisdom", "loyalty", "tranquility"],
        "brand_fit": ["finance", "technology", "healthcare", "corporate"]
    },
    "navy": {
        "emotions": ["authoritative", "traditional", "reliable", "professional", "strong"],
        "associations": ["authority", "tradition", "security", "intelligence"],
        "brand_fit": ["corporate", "educational", "military", "professional services"]
    },
    "sky blue": {
        "emotions": ["peaceful", "tranquil", "light", "airy", "open"],
        "associations": ["sky", "freedom", "inspiration", "air", "clarity"],
        "brand_fit": ["air travel", "cloud services", "mindfulness apps", "children's brands"]
    },
    
    # Purples
    "purple": {
        "emotions": ["creative", "royal", "mysterious", "spiritual", "luxurious"],
        "associations": ["luxury", "creativity", "wisdom", "mystery", "quality"],
        "brand_fit": ["luxury goods", "creative services", "spirituality", "anti-aging"]
    },
    "lavender": {
        "emotions": ["soothing", "gentle", "feminine", "nostalgic", "romantic"],
        "associations": ["flowers", "relaxation", "femininity", "spring"],
        "brand_fit": ["spa", "wellness", "wedding services", "aromatherapy"]
    },
    "indigo": {
        "emotions": ["intuitive", "contemplative", "deep", "mysterious", "dignified"],
        "associations": ["night sky", "depth", "perception", "intuition"],
        "brand_fit": ["spiritual products", "sleep aids", "mindfulness", "sophisticated design"]
    },
    
    # Pinks
    "pink": {
        "emotions": ["romantic", "feminine", "playful", "compassionate", "nurturing"],
        "associations": ["love", "femininity", "youth", "sweetness", "compassion"],
        "brand_fit": ["beauty", "children's products", "confectionery", "feminine products"]
    },
    "rose": {
        "emotions": ["romantic", "nostalgic", "soft", "sentimental", "refined"],
        "associations": ["flowers", "romance", "femininity", "tenderness"],
        "brand_fit": ["romantic products", "vintage brands", "cosmetics", "floral products"]
    },
    "fuchsia": {
        "emotions": ["vibrant", "energetic", "confident", "youthful", "bold"],
        "associations": ["energy", "flamboyance", "confidence", "fashion"],
        "brand_fit": ["fashion", "cosmetics", "youth brands", "entertainment"]
    },
    
    # Browns
    "brown": {
        "emotions": ["reliable", "sturdy", "warm", "natural", "grounded"],
        "associations": ["earth", "wood", "outdoors", "reliability", "comfort"],
        "brand_fit": ["coffee", "chocolate", "craftsmanship", "outdoors", "furniture"]
    },
    "beige": {
        "emotions": ["calm", "neutral", "versatile", "classic", "understated"],
        "associations": ["sand", "neutrality", "background", "simplicity", "foundation"],
        "brand_fit": ["luxury", "minimalist design", "cosmetics", "high-end fashion"]
    },
    "tan": {
        "emotions": ["natural", "earthy", "versatile", "welcoming", "warm"],
        "associations": ["leather", "wood", "natural materials", "warmth"],
        "brand_fit": ["leather goods", "outdoor products", "neutral fashion", "coffee shops"]
    },
    "chocolate": {
        "emotions": ["rich", "indulgent", "warm", "luxurious", "comforting"],
        "associations": ["indulgence", "richness", "sweetness", "depth", "comfort"],
        "brand_fit": ["confectionery", "luxury goods", "coffee", "gourmet foods"]
    },
    
    # Neutrals
    "gray": {
        "emotions": ["neutral", "balanced", "professional", "sophisticated", "timeless"],
        "associations": ["formality", "neutrality", "subtlety", "professionalism"],
        "brand_fit": ["business", "technology", "luxury", "minimal designs"]
    },
    "silver": {
        "emotions": ["sleek", "modern", "technological", "refined", "elegant"],
        "associations": ["technology", "modernity", "sophistication", "prestige"],
        "brand_fit": ["technology", "automotive", "luxury brands", "modern design"]
    },
    "charcoal": {
        "emotions": ["sophisticated", "strong", "solid", "reserved", "serious"],
        "associations": ["professionalism", "strength", "formality", "structure"],
        "brand_fit": ["business services", "luxury brands", "men's products", "professional tools"]
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
    },
    "ivory": {
        "emotions": ["classic", "soft", "warm", "elegant", "timeless"],
        "associations": ["tradition", "elegance", "subtlety", "warmth", "heritage"],
        "brand_fit": ["bridal", "luxury papers", "cosmetics", "high-end fashion"]
    }
}

# Improved harmony psychology effects with design-relevant terminology
HARMONY_EFFECTS = {
    "complementary": "Creates a vibrant, high-contrast palette that commands attention. Ideal for brands wanting to stand out or create visual energy. Effective for call-to-action elements and creating bold visual impact.",
    "analogous": "Creates a harmonious, cohesive palette with natural flow and low visual tension. Perfect for creating a unified, professional look that feels balanced and intentionally designed.",
    "triadic": "Offers visual vibrancy while maintaining perceptual balance. Well-suited for creative and playful brands that still need visual harmony and compositional integrity.",
    "tetradic": "Provides a rich, varied palette with multiple accent possibilities. Excellent for brands with diverse product lines or complex visual communication needs.",
    "monochromatic": "Creates a sophisticated, cohesive palette with subtle depth. Particularly effective for luxury brands, minimalist designs, and contexts where content should be the focal point."
}

def identify_color_name(hsv):
    """Identify detailed color name based on HSV values.
    
    Args:
        hsv (tuple): HSV color values (h, s, v) with h in range 0-1
        
    Returns:
        str: Detailed color name
    """
    h, s, v = hsv
    
    # Convert h to degrees (0-360)
    h_deg = h * 360
    
    # Handle grayscale and near-grayscale colors
    if s < 0.12:  # Very low saturation indicates grayscale
        if v < 0.10:  # Very dark
            return "black"
        elif v < 0.25:  # Dark
            return "charcoal"
        elif v < 0.60:  # Mid-tone
            return "gray"
        elif v < 0.90:  # Light
            return "silver"
        else:  # Very light
            return "white"
    
    # Handle very dark colors (nearly black) regardless of hue
    if v < 0.12:
        return "black"
    
    # Handle off-whites and ivories
    if v > 0.85 and s < 0.20:
        if h_deg >= 30 and h_deg < 90:  # Warm off-white
            return "ivory"
        else:  # Cool or neutral off-white
            return "white"
    
    # Handle browns (low value, low-to-mid saturation, in red-yellow range)
    if v < 0.65 and s < 0.65 and ((h_deg >= 0 and h_deg < 60) or h_deg >= 330):
        if v < 0.20:  # Very dark brown
            return "chocolate"
        elif v < 0.35:  # Dark brown
            return "brown"
        elif v < 0.55:  # Medium brown
            if h_deg > 20 and h_deg < 40 and s > 0.40:  # More orange-brown
                return "terracotta"
            else:
                return "brown"
        else:  # Light brown
            if s < 0.35:  # Low saturation light brown
                return "beige"
            else:  # Medium-high saturation light brown
                return "tan"
    
    # Handle different hue ranges with nuanced names
    # Reds (0-10, 350-360)
    if (h_deg < 10 or h_deg >= 350) and s > 0.20:
        if v < 0.40:
            return "burgundy"
        elif v < 0.60:
            return "crimson"
        else:
            return "red"
    
    # Oranges (10-40)
    elif h_deg < 40 and s > 0.20:
        if v < 0.50:
            return "terracotta"
        elif h_deg > 25 and s > 0.60 and v > 0.80:
            return "coral"
        else:
            return "orange"
    
    # Yellows (40-70)
    elif h_deg < 70 and s > 0.20:
        if s > 0.50 and v > 0.80:  # Bright and saturated
            return "yellow"
        elif v > 0.70 and s > 0.50:  # Bright but less saturated
            return "gold"
        else:  # Darker yellow
            return "mustard"
    
    # Greens (70-160)
    elif h_deg < 160 and s > 0.15:
        if h_deg < 80 and v < 0.60:  # Yellow-green, darker
            return "olive"
        elif h_deg > 140 and v > 0.70:  # Blue-green, lighter
            return "mint"
        elif s < 0.40 and v < 0.70:  # Less saturated, medium-dark
            return "sage"
        else:
            return "green"
    
    # Teals/Cyans (160-195)
    elif h_deg < 195 and s > 0.15:
        return "teal"
    
    # Blues (195-240)
    elif h_deg < 240 and s > 0.15:
        if s > 0.30 and v < 0.50:  # Dark and moderately saturated
            return "navy"
        elif v > 0.75 and s < 0.50:  # Light and less saturated
            return "sky blue"
        else:
            return "blue"
    
    # Purples (240-290)
    elif h_deg < 290 and s > 0.15:
        if h_deg < 260 and s > 0.50 and v < 0.60:  # Deep purple-blue
            return "indigo"
        elif v > 0.70 and s < 0.50:  # Light and less saturated
            return "lavender"
        else:
            return "purple"
    
    # Pinks (290-350)
    elif h_deg < 350 and s > 0.15:
        if s > 0.70 and v > 0.70:  # Bright and highly saturated
            return "fuchsia"
        elif h_deg < 320 and s < 0.60:  # Less saturated, more muted
            return "rose"
        else:
            return "pink"
    
    # Default fallback - should rarely be reached with above logic
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
        
        # Identify color name with improved function
        color_name = identify_color_name((h, s, v))
        color_names.append(color_name)
        
        # Get emotional associations - fall back to basic color if specific shade not found
        base_color = color_name
        if color_name not in COLOR_EMOTIONS:
            # Map specific shades to their base colors for emotion lookup
            color_mapping = {
                "burgundy": "red", "crimson": "red",
                "terracotta": "orange", "coral": "orange",
                "gold": "yellow", "mustard": "yellow",
                "sage": "green", "mint": "green", "olive": "green",
                "navy": "blue", "sky blue": "blue",
                "lavender": "purple", "indigo": "purple",
                "rose": "pink", "fuchsia": "pink",
                "beige": "brown", "tan": "brown", "chocolate": "brown",
                "charcoal": "gray", "silver": "gray",
                "ivory": "white"
            }
            base_color = color_mapping.get(color_name, "gray")
        
        emotions = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("emotions", [])
        associations = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("associations", [])
        brand_fit = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("brand_fit", [])
        
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
        # Group similar colors for harmony analysis
        base_name = name
        # Map specific shades to their base colors for harmony analysis
        color_groups = {
            "burgundy": "red", "crimson": "red",
            "terracotta": "orange", "coral": "orange",
            "gold": "yellow", "mustard": "yellow",
            "sage": "green", "mint": "green", "olive": "green",
            "navy": "blue", "sky blue": "blue",
            "lavender": "purple", "indigo": "purple",
            "rose": "pink", "fuchsia": "pink",
            "beige": "brown", "tan": "brown", "chocolate": "brown",
            "charcoal": "gray", "silver": "gray",
            "ivory": "white"
        }
        base_name = color_groups.get(name, name)
        
        if base_name in color_name_counts:
            color_name_counts[base_name] += 1
        else:
            color_name_counts[base_name] = 1
    
    # Store original color names for display
    unique_colors = list(set(color_names))
    
    color_diversity = len(color_name_counts)
    
    # Analyze harmony
    base_colors = list(color_name_counts.keys())
    has_complementary = len(set(["red", "green"]).intersection(set(base_colors))) == 2 or \
                       len(set(["blue", "orange"]).intersection(set(base_colors))) == 2 or \
                       len(set(["yellow", "purple"]).intersection(set(base_colors))) == 2
                       
    has_analogous = any(
        sum(1 for name in base_colors if name in group) >= 3
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
        industry_fits = []
        for color in primary_colors[:2]:  # Use top two colors
            if color in COLOR_EMOTIONS:
                industry_fits.extend(COLOR_EMOTIONS[color]["brand_fit"])
        
        top_industries = list(set(industry_fits))[:3]  # Get unique industries, limit to top 3
        
        emotion_str = ", ".join(results["overall"]["dominant_emotions"])
        industry_str = ", ".join(top_industries) if top_industries else "various industries"
        color_str = ", ".join(unique_colors[:4])  # List up to 4 unique color names
        
        recommendations = f"This color palette features {color_str} and evokes feelings of {emotion_str}. "
        recommendations += f"It would be well-suited for brands in {industry_str}. "
        
        # Improved harmony description with guaranteed correct sentence structure
        if dominant_harmony:
            harmony_effect = HARMONY_EFFECTS.get(dominant_harmony, "a balanced visual effect")
            
            # Extract first word to check for potential redundancy
            first_word = harmony_effect.split()[0].lower()
            
            if first_word == "creates":
                # If harmony effect starts with "Creates", extract everything after that word
                effect_content = harmony_effect[len("Creates"):].strip()
                # And start with a clean sentence
                recommendations += f"The {dominant_harmony} color relationship creates{effect_content} "
            elif first_word in ["offers", "provides"]:
                # If it starts with another verb, reword the sentence to avoid redundancy
                verb = first_word
                effect_content = harmony_effect[len(verb):].strip()
                recommendations += f"The {dominant_harmony} color relationship {verb}{effect_content} "
            else:
                # For any other pattern, use a generic connector
                recommendations += f"The {dominant_harmony} color relationship delivers {harmony_effect[0].lower() + harmony_effect[1:]} "
        
        results["overall"]["brand_recommendations"] = recommendations
    
    return results
