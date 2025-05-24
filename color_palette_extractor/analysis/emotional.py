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
    "maroon": {
        "emotions": ["serious", "controlled", "thoughtful", "intense", "mature"],
        "associations": ["autumn", "earth", "stability", "confidence"],
        "brand_fit": ["universities", "law firms", "financial services", "heritage brands"]
    },
    "scarlet": {
        "emotions": ["vivid", "adventurous", "confident", "courageous", "luxurious"],
        "associations": ["passion", "luxury", "courage", "nobility"],
        "brand_fit": ["luxury fashion", "sports cars", "premium cosmetics", "high-end retail"]
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
    "apricot": {
        "emotions": ["gentle", "warm", "approachable", "soft", "inviting"],
        "associations": ["comfort", "hospitality", "freshness", "care"],
        "brand_fit": ["hospitality", "baby products", "wellness", "home goods"]
    },
    "peach": {
        "emotions": ["friendly", "warm", "caring", "gentle", "soft"],
        "associations": ["health", "vitality", "youthfulness", "sweetness"],
        "brand_fit": ["beauty products", "health foods", "children's brands", "hospitality"]
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
    "amber": {
        "emotions": ["energizing", "glowing", "rich", "warm", "inviting"],
        "associations": ["honey", "precious stones", "ancient", "preservation"],
        "brand_fit": ["jewelry", "perfume", "craft beverages", "luxury goods"]
    },
    "lemon": {
        "emotions": ["zesty", "fresh", "energetic", "clean", "vibrant"],
        "associations": ["citrus", "freshness", "cleanliness", "summer"],
        "brand_fit": ["cleaning products", "beverages", "summer products", "fresh foods"]
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
    "emerald": {
        "emotions": ["luxurious", "vibrant", "sophisticated", "rich", "regal"],
        "associations": ["precious stones", "wealth", "growth", "harmony"],
        "brand_fit": ["jewelry", "luxury brands", "high-end fashion", "premium services"]
    },
    "forest": {
        "emotions": ["deep", "mysterious", "strong", "natural", "protective"],
        "associations": ["wilderness", "strength", "depth", "shelter"],
        "brand_fit": ["outdoor equipment", "environmental organizations", "men's products", "adventure brands"]
    },
    "lime": {
        "emotions": ["vibrant", "energetic", "fresh", "youthful", "modern"],
        "associations": ["citrus", "energy", "technology", "innovation"],
        "brand_fit": ["energy drinks", "tech startups", "youth brands", "sports products"]
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
    "turquoise": {
        "emotions": ["refreshing", "tropical", "calming", "clear", "sophisticated"],
        "associations": ["ocean", "gemstones", "clarity", "communication"],
        "brand_fit": ["travel", "spa & wellness", "jewelry", "water sports"]
    },
    "cobalt": {
        "emotions": ["bold", "electric", "dynamic", "modern", "confident"],
        "associations": ["technology", "innovation", "depth", "vibrancy"],
        "brand_fit": ["tech companies", "sports brands", "modern design", "automotive"]
    },
    "periwinkle": {
        "emotions": ["serene", "soft", "nostalgic", "gentle", "dreamy"],
        "associations": ["flowers", "calmness", "imagination", "serenity"],
        "brand_fit": ["children's products", "home decor", "creative services", "wellness"]
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
    "violet": {
        "emotions": ["imaginative", "sensitive", "artistic", "mystical", "unique"],
        "associations": ["creativity", "imagination", "spirituality", "individuality"],
        "brand_fit": ["art supplies", "creative agencies", "alternative medicine", "boutique brands"]
    },
    "plum": {
        "emotions": ["rich", "sophisticated", "dramatic", "elegant", "mature"],
        "associations": ["depth", "luxury", "autumn", "richness"],
        "brand_fit": ["wine brands", "luxury fashion", "upscale restaurants", "premium cosmetics"]
    },
    "mauve": {
        "emotions": ["delicate", "refined", "understated", "vintage", "feminine"],
        "associations": ["nostalgia", "elegance", "subtlety", "romance"],
        "brand_fit": ["vintage fashion", "wedding services", "boutique hotels", "artisanal products"]
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
    "salmon": {
        "emotions": ["warm", "friendly", "approachable", "energetic", "healthy"],
        "associations": ["warmth", "vitality", "freshness", "health"],
        "brand_fit": ["health foods", "fitness", "wellness products", "hospitality"]
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
    "taupe": {
        "emotions": ["sophisticated", "timeless", "flexible", "calming", "elegant"],
        "associations": ["neutrality", "sophistication", "versatility", "refinement"],
        "brand_fit": ["interior design", "luxury fashion", "architectural firms", "premium brands"]
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
    },
    "cream": {
        "emotions": ["gentle", "warm", "soothing", "classic", "comfortable"],
        "associations": ["softness", "comfort", "luxury", "natural"],
        "brand_fit": ["dairy products", "bedding", "luxury hotels", "natural cosmetics"]
    }
}

HARMONY_EFFECTS = {
    "complementary": "vibrant, high-contrast palette that commands attention. Ideal for brands wanting to stand out or create visual energy. Effective for call-to-action elements and creating bold visual impact",
    "analogous": "harmonious, cohesive palette with natural flow and low visual tension. Perfect for creating a unified, professional look that feels balanced and intentionally designed",
    "triadic": "visual vibrancy while maintaining perceptual balance. Well-suited for creative and playful brands that still need visual harmony and compositional integrity",
    "tetradic": "rich, varied palette with multiple accent possibilities. Excellent for brands with diverse product lines or complex visual communication needs",
    "monochromatic": "sophisticated, cohesive palette with subtle depth. Particularly effective for luxury brands, minimalist designs, and contexts where content should be the focal point"
}

def identify_color_name(hsv):
    """Identify detailed color name based on HSV values.
    
    Args:
        hsv (tuple): HSV color values (h, s, v) with h in range 0-1
        
    Returns:
        str: Detailed color name
    """
    h, s, v = hsv
    h_deg = h * 360
    
    if s < 0.08:
        if v < 0.10:
            return "black"
        elif v < 0.25:
            return "charcoal"
        elif v < 0.60:
            return "gray"
        elif v < 0.90:
            return "silver"
        else:
            return "white"
    
    if v < 0.12:
        return "black"
    
    if v > 0.90 and s < 0.15:
        if h_deg >= 30 and h_deg < 60:
            return "cream"
        elif h_deg >= 15 and h_deg < 30:
            return "ivory"
        else:
            return "white"
    
    if v < 0.65 and s < 0.65 and ((h_deg >= 0 and h_deg < 60) or h_deg >= 330):
        if v < 0.20:
            return "chocolate"
        elif v < 0.35:
            return "brown"
        elif v < 0.55:
            if h_deg > 20 and h_deg < 40 and s > 0.40:
                return "terracotta"
            else:
                return "brown"
        else:
            if s < 0.25:
                return "taupe"
            elif s < 0.35:
                return "beige"
            else:
                return "tan"
    
    if (h_deg < 10 or h_deg >= 350) and s > 0.20:
        if v < 0.35:
            return "maroon"
        elif v < 0.50:
            return "burgundy"
        elif v < 0.65:
            return "crimson"
        elif s > 0.80:
            return "scarlet"
        else:
            return "red"
    
    elif h_deg < 25 and s > 0.20:
        if v > 0.85 and s < 0.50:
            return "salmon"
        elif v > 0.80 and s < 0.40:
            return "peach"
        elif h_deg > 15:
            return "coral"
        else:
            return "red"
    
    elif h_deg < 40 and s > 0.20:
        if v < 0.50:
            return "terracotta"
        elif v > 0.85 and s < 0.50:
            return "apricot"
        elif v > 0.80 and s < 0.60:
            return "peach"
        elif h_deg > 25 and s > 0.60 and v > 0.80:
            return "coral"
        else:
            return "orange"
    
    elif h_deg < 55 and s > 0.20:
        if s > 0.80 and v > 0.85:
            return "amber"
        elif v > 0.85 and s > 0.70:
            return "gold"
        elif v < 0.70:
            return "mustard"
        else:
            return "yellow"
    
    elif h_deg < 70 and s > 0.20:
        if s > 0.85 and v > 0.90:
            return "lemon"
        elif s > 0.50 and v > 0.80:
            return "yellow"
        elif v > 0.70 and s > 0.50:
            return "gold"
        else:
            return "mustard"
    
    elif h_deg < 90 and s > 0.15:
        if h_deg < 80 and v < 0.60:
            return "olive"
        elif s > 0.80 and v > 0.80:
            return "lime"
        else:
            return "green"
    
    elif h_deg < 150 and s > 0.15:
        if v < 0.40:
            return "forest"
        elif h_deg > 140 and v > 0.70:
            return "mint"
        elif s < 0.40 and v < 0.70:
            return "sage"
        elif s > 0.70 and v > 0.70:
            return "emerald"
        else:
            return "green"
    
    elif h_deg < 195 and s > 0.15:
        if h_deg > 180:
            return "turquoise"
        else:
            return "teal"
    
    elif h_deg < 240 and s > 0.15:
        if s > 0.30 and v < 0.50:
            return "navy"
        elif v > 0.75 and s < 0.50:
            return "sky blue"
        elif s > 0.80 and v > 0.70:
            return "cobalt"
        else:
            return "blue"
    
    elif h_deg < 260 and s > 0.15:
        if s > 0.50 and v < 0.60:
            return "indigo"
        elif v > 0.80 and s < 0.40:
            return "periwinkle"
        else:
            return "blue"
    
    elif h_deg < 290 and s > 0.15:
        if h_deg < 270 and v > 0.70 and s < 0.50:
            return "lavender"
        elif v < 0.50:
            return "plum"
        elif s < 0.50:
            return "mauve"
        elif h_deg < 280:
            return "violet"
        else:
            return "purple"
    
    elif h_deg < 350 and s > 0.15:
        if s > 0.70 and v > 0.70:
            return "fuchsia"
        elif h_deg < 320 and s < 0.60:
            return "rose"
        else:
            return "pink"
    
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
    
    for i, color in enumerate(color_palette):
        hex_color, rgb, cmyk = color
        
        r, g, b = [val/255 for val in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        color_name = identify_color_name((h, s, v))
        color_names.append(color_name)
        
        base_color = color_name
        if color_name not in COLOR_EMOTIONS:
            color_mapping = {
                "burgundy": "red", "crimson": "red", "maroon": "red", "scarlet": "red",
                "terracotta": "orange", "coral": "orange", "apricot": "orange", "peach": "orange",
                "gold": "yellow", "mustard": "yellow", "amber": "yellow", "lemon": "yellow",
                "sage": "green", "mint": "green", "olive": "green", "emerald": "green", 
                "forest": "green", "lime": "green",
                "navy": "blue", "sky blue": "blue", "turquoise": "blue", "cobalt": "blue", 
                "periwinkle": "blue",
                "lavender": "purple", "indigo": "purple", "violet": "purple", "plum": "purple", 
                "mauve": "purple",
                "rose": "pink", "fuchsia": "pink", "salmon": "pink",
                "beige": "brown", "tan": "brown", "chocolate": "brown", "taupe": "brown",
                "charcoal": "gray", "silver": "gray",
                "ivory": "white", "cream": "white"
            }
            base_color = color_mapping.get(color_name, "gray")
        
        emotions = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("emotions", [])
        associations = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("associations", [])
        brand_fit = COLOR_EMOTIONS.get(color_name, COLOR_EMOTIONS.get(base_color, {})).get("brand_fit", [])
        
        color_result = {
            "hex": hex_color,
            "color_name": color_name,
            "emotions": emotions,
            "associations": associations,
            "brand_fit": brand_fit,
            "intensity": "strong" if s > 0.7 and v > 0.7 else "moderate" if s > 0.4 else "subtle"
        }
        results["colors"].append(color_result)
        
        for emotion in emotions:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1
    
    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
    results["overall"]["dominant_emotions"] = [emotion for emotion, count in sorted_emotions[:3]]
    
    color_name_counts = {}
    for name in color_names:
        base_name = name
        color_groups = {
            "burgundy": "red", "crimson": "red", "maroon": "red", "scarlet": "red",
            "terracotta": "orange", "coral": "orange", "apricot": "orange", "peach": "orange",
            "gold": "yellow", "mustard": "yellow", "amber": "yellow", "lemon": "yellow",
            "sage": "green", "mint": "green", "olive": "green", "emerald": "green",
            "forest": "green", "lime": "green",
            "navy": "blue", "sky blue": "blue", "turquoise": "blue", "cobalt": "blue",
            "periwinkle": "blue",
            "lavender": "purple", "indigo": "purple", "violet": "purple", "plum": "purple",
            "mauve": "purple",
            "rose": "pink", "fuchsia": "pink", "salmon": "pink",
            "beige": "brown", "tan": "brown", "chocolate": "brown", "taupe": "brown",
            "charcoal": "gray", "silver": "gray",
            "ivory": "white", "cream": "white"
        }
        base_name = color_groups.get(name, name)
        
        if base_name in color_name_counts:
            color_name_counts[base_name] += 1
        else:
            color_name_counts[base_name] = 1
    
    unique_colors = list(set(color_names))
    
    color_diversity = len(color_name_counts)
    
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
        dominant_harmony = "mixed"
    
    if dominant_harmony in HARMONY_EFFECTS:
        results["overall"]["harmony_analysis"] = HARMONY_EFFECTS[dominant_harmony]
    else:
        results["overall"]["harmony_analysis"] = "Mixed color harmony providing a balanced visual effect."
    
    primary_colors = [name for name, count in sorted(color_name_counts.items(), key=lambda x: x[1], reverse=True)]
    
    if not primary_colors:
        results["overall"]["brand_recommendations"] = "Unable to determine brand recommendations."
    else:
        industry_fits = []
        for color in primary_colors[:2]:
            if color in COLOR_EMOTIONS:
                industry_fits.extend(COLOR_EMOTIONS[color]["brand_fit"])
        
        top_industries = list(set(industry_fits))[:3]
        
        emotion_str = ", ".join(results["overall"]["dominant_emotions"])
        industry_str = ", ".join(top_industries) if top_industries else "various industries"
        color_str = ", ".join(unique_colors[:4])
        
        recommendations = f"This color palette features {color_str} and evokes feelings of {emotion_str}. "
        recommendations += f"It would be well-suited for brands in {industry_str}. "
        
        if dominant_harmony and dominant_harmony in HARMONY_EFFECTS:
            harmony_effect = HARMONY_EFFECTS[dominant_harmony]
            recommendations += f"The {dominant_harmony} color relationship creates a {harmony_effect}."
        
        results["overall"]["brand_recommendations"] = recommendations
    
    return results
