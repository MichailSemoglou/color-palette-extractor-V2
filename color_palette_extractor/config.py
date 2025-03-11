#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration management for the Color Palette Extractor.
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "num_colors": 6,
    "max_dimension": 1000,
    "output_dir": "output",
    "generate_pdf": True,
    "generate_text": True,
    "parallel_jobs": None,  # Auto-detect CPU count
    "use_cache": True,
    "cache_dir": ".cache",
    "cache_max_age_days": 30,
    "pdf_options": {
        "page_size": "A4",
        "margin": 36,  # 0.5 inch in points
        "show_original_image": True,
        "image_width": 216  # 3 inches in points
    },
    "fonts": {
        "title": "Inter-Bold",
        "body": "Inter-Regular",
        "fallback": "Helvetica"
    },
    "harmonies": {
        "complementary": True,
        "analogous": True,
        "triadic": True,
        "tetradic": True,
        "tints": True,
        "shades": True
    }
}

class ConfigManager:
    """Manages configuration for the color palette extractor."""
    
    def __init__(self, config_path=None):
        """Initialize ConfigManager with optional path to config file.
        
        Args:
            config_path (str, optional): Path to configuration file
                If None, uses ~/.color_extractor_config.json or default config
        """
        self.config_path = config_path or os.path.expanduser("~/.color_extractor_config.json")
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file, or create default if not exists.
        
        Returns:
            dict: Loaded configuration dictionary
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded configuration from {self.config_path}")
                
                # Merge with default config to ensure all keys exist
                merged_config = DEFAULT_CONFIG.copy()
                self._deep_update(merged_config, config)
                return merged_config
            else:
                logger.info(f"No configuration file found at {self.config_path}, using defaults")
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            logger.warning("Using default configuration")
            return DEFAULT_CONFIG.copy()
    
    def _deep_update(self, target, source):
        """Recursively update nested dictionaries.
        
        Args:
            target (dict): Target dictionary to update
            source (dict): Source dictionary with new values
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def save_config(self, config_path=None):
        """Save current configuration to file.
        
        Args:
            config_path (str, optional): Path to save configuration file
                If None, uses the current config_path
                
        Returns:
            bool: True if successful, False otherwise
        """
        save_path = config_path or self.config_path
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Saved configuration to {save_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value.
        
        Args:
            key (str): Configuration key, can use dot notation for nested keys
            default: Default value if key not found
            
        Returns:
            Value for the key or default if not found
        """
        try:
            if '.' in key:
                # Handle nested keys with dot notation
                parts = key.split('.')
                value = self.config
                for part in parts:
                    value = value.get(part, {})
                    
                # Check if we reached the end with a valid value
                if value == {} and len(parts) > 0:
                    return default
                return value
            else:
                return self.config.get(key, default)
        except:
            return default
    
    def set(self, key, value):
        """Set a configuration value.
        
        Args:
            key (str): Configuration key, can use dot notation for nested keys
            value: Value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if '.' in key:
                # Handle nested keys with dot notation
                parts = key.split('.')
                config = self.config
                
                # Navigate to the innermost dict
                for part in parts[:-1]:
                    if part not in config:
                        config[part] = {}
                    config = config[part]
                
                # Set the value
                config[parts[-1]] = value
            else:
                self.config[key] = value
            
            return True
        except:
            logger.error(f"Error setting configuration key '{key}'")
            return False
    
    def get_harmony_types(self):
        """Get enabled harmony types.
        
        Returns:
            list: List of enabled harmony types
        """
        harmonies = self.config.get('harmonies', {})
        return [
            harmony_type for harmony_type, enabled in harmonies.items()
            if enabled
        ]
    
    def get_cache_settings(self):
        """Get cache settings.
        
        Returns:
            dict: Cache settings
        """
        return {
            'enabled': self.config.get('use_cache', True),
            'cache_dir': self.config.get('cache_dir', '.cache'),
            'max_age_days': self.config.get('cache_max_age_days', 30)
        }
    
    def get_pdf_options(self):
        """Get PDF output options.
        
        Returns:
            dict: PDF options
        """
        return self.config.get('pdf_options', {})
    
    def reset_to_defaults(self):
        """Reset configuration to defaults.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.config = DEFAULT_CONFIG.copy()
            logger.info("Reset configuration to defaults")
            return True
        except:
            logger.error("Error resetting configuration to defaults")
            return False
