#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caching utilities for the Color Palette Extractor 2.0
"""

import os
import pickle
import hashlib
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages caching of extracted color palettes to avoid reprocessing."""
    
    def __init__(self, cache_dir=".cache", max_age_days=30):
        """Initialize the cache manager.
        
        Args:
            cache_dir (str): Directory to store cache files
            max_age_days (int): Maximum age of cache files in days
        """
        self.cache_dir = cache_dir
        self.max_age_days = max_age_days
        
        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_cache_key(self, image_path, num_colors):
        """Generate a cache key for an image and number of colors.
        
        Args:
            image_path (str): Path to the image file
            num_colors (int): Number of colors to extract
            
        Returns:
            str: Cache key
        """
        # Get file modification time and size for cache invalidation
        stat = os.stat(image_path)
        file_meta = f"{os.path.basename(image_path)}_{stat.st_mtime}_{stat.st_size}_{num_colors}"
        
        # Generate a hash of the metadata
        return hashlib.md5(file_meta.encode()).hexdigest()
    
    def get_cache_path(self, cache_key):
        """Get the cache file path for a cache key.
        
        Args:
            cache_key (str): Cache key
            
        Returns:
            str: Path to the cache file
        """
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    
    def get_cached_result(self, image_path, num_colors):
        """Get a cached result for an image if available.
        
        Args:
            image_path (str): Path to the image file
            num_colors (int): Number of colors to extract
            
        Returns:
            object or None: Cached result or None if not available
        """
        try:
            cache_key = self.get_cache_key(image_path, num_colors)
            cache_path = self.get_cache_path(cache_key)
            
            if os.path.exists(cache_path):
                # Check if cache is too old
                cache_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
                if datetime.now() - cache_time > timedelta(days=self.max_age_days):
                    logger.debug(f"Cache expired for {image_path}")
                    return None
                
                # Load cached result
                with open(cache_path, 'rb') as f:
                    result = pickle.load(f)
                logger.debug(f"Loaded cached result for {image_path}")
                return result
                
        except Exception as e:
            logger.warning(f"Error getting cached result for {image_path}: {str(e)}")
            
        return None
    
    def store_result(self, image_path, num_colors, result):
        """Store a result in the cache.
        
        Args:
            image_path (str): Path to the image file
            num_colors (int): Number of colors extracted
            result: Result to cache
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cache_key = self.get_cache_key(image_path, num_colors)
            cache_path = self.get_cache_path(cache_key)
            
            with open(cache_path, 'wb') as f:
                pickle.dump(result, f)
            logger.debug(f"Cached result for {image_path}")
            return True
            
        except Exception as e:
            logger.warning(f"Error caching result for {image_path}: {str(e)}")
            return False
    
    def clear_cache(self, max_age_days=None):
        """Clear old cache files.
        
        Args:
            max_age_days (int, optional): Maximum age of files to keep
                If None, uses the instance's max_age_days
                
        Returns:
            int: Number of files removed
        """
        max_age = max_age_days if max_age_days is not None else self.max_age_days
        count = 0
        
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age)
            
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        count += 1
                        
            logger.info(f"Cleared {count} old cache files")
            return count
            
        except Exception as e:
            logger.warning(f"Error clearing cache: {str(e)}")
            return 0
