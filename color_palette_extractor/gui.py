#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Graphical user interface for the Color Palette Extractor 2.0
"""

import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from datetime import datetime
from PIL import Image, ImageTk

from .. import __version__
from .core import extract_color_palette
from .harmonies import get_harmonies
from color_palette_extractor.output.pdf import save_palette_to_pdf
from color_palette_extractor.output.text import save_palette_and_harmonies
from .batch import process_images, process_folder
from color_palette_extractor.utils.image import find_images_in_directory, is_valid_image
from .config import ConfigManager

logger = logging.getLogger(__name__)

class ColorPaletteExtractorGUI:
    """Graphical user interface for the Color Palette Extractor."""
    
    def __init__(self, root):
        """Initialize the GUI.
        
        Args:
            root (tk.Tk): Root Tkinter window
        """
        self.root = root
        self.root.title(f"Color Palette Extractor v{__version__}")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Load configuration
        self.config_manager = ConfigManager()
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value=self.config_manager.get('output_dir', os.path.join(os.getcwd(), "output")))
        self.num_colors = tk.IntVar(value=self.config_manager.get('num_colors', 6))
        self.recursive = tk.BooleanVar(value=False)
        self.use_cache = tk.BooleanVar(value=self.config_manager.get('use_cache', True))
        self.generate_pdf = tk.BooleanVar(value=self.config_manager.get('generate_pdf', True))
        self.generate_text = tk.BooleanVar(value=self.config_manager.get('generate_text', True))
        self.processing = False
        self.preview_image = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Configure logging
        self.setup_logging()
        
        logger.info(f"GUI initialized (Color Palette Extractor v{__version__})")
    
    def setup_logging(self):
        """Configure logging for the GUI."""
        # Create log directory
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create timestamp for log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"color_extractor_gui_{timestamp}.log")
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Add file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        root_logger.addHandler(file_handler)
        
        # Create handler that writes to the log text widget
        class TextWidgetHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
                
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.configure(state='normal')
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)
                    self.text_widget.configure(state='disabled')
                # This is necessary because this handler might be called from
                # a thread other than the main thread
                self.text_widget.after(0, append)
        
        # Add handler to write to text widget
        text_handler = TextWidgetHandler(self.log_text)
        text_handler.setLevel(logging.INFO)
        text_handler.setFormatter(logging.Formatter('%(message)s'))
        root_logger.addHandler(text_handler)
    
    def create_widgets(self):
        """Create GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Input Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, padx=5)
        
        ttk.Button(button_frame, text="Select File", command=self.select_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT, padx=2)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(output_frame, text="Browse", command=self.select_output_folder).grid(row=0, column=2, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=5)
        
        # Column 1
        ttk.Label(options_frame, text="Number of Colors:").grid(row=0, column=0, sticky=tk.W, pady=5)
        color_spinner = ttk.Spinbox(options_frame, from_=1, to=12, textvariable=self.num_colors, width=5)
        color_spinner.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Column 2
        ttk.Checkbutton(options_frame, text="Process Subfolders", variable=self.recursive).grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)
        ttk.Checkbutton(options_frame, text="Use Cache", variable=self.use_cache).grid(row=1, column=2, sticky=tk.W, padx=20, pady=5)
        
        # Column 3
        ttk.Checkbutton(options_frame, text="Generate PDF", variable=self.generate_pdf).grid(row=0, column=3, sticky=tk.W, padx=20, pady=5)
        ttk.Checkbutton(options_frame, text="Generate Text", variable=self.generate_text).grid(row=1, column=3, sticky=tk.W, padx=20, pady=5)
        
        # Preview and progress area
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image preview
        preview_frame = ttk.LabelFrame(bottom_frame, text="Preview")
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.preview_canvas = tk.Canvas(preview_frame, bg="white")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log and progress
        log_frame = ttk.LabelFrame(bottom_frame, text="Log")
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.log_text = tk.Text(log_frame, height=10, width=40, wrap=tk.WORD)
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.configure(state='disabled')
        
        # Add scrollbar to log
        log_scrollbar = ttk.Scrollbar(self.log_text, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.progress_bar = ttk.Progressbar(log_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Bottom buttons
        button_bar = ttk.Frame(main_frame)
        button_bar.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_bar, text="Process", command=self.start_processing).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_bar, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_bar, text="About", command=self.show_about).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log_message(self, message):
        """Add a message to the log text widget.
        
        Args:
            message (str): Message to add
        """
        logger.info(message)
    
    def select_file(self):
        """Open file dialog to select an image file."""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"), ("All files", "*.*")]
        )
        if file_path:
            self.input_path.set(file_path)
            self.update_preview(file_path)
    
    def select_folder(self):
        """Open folder dialog to select an image folder."""
        folder_path = filedialog.askdirectory(title="Select Image Folder")
        if folder_path:
            self.input_path.set(folder_path)
            self.update_preview(None)
            self.log_message(f"Selected folder: {folder_path}")
            
            # Count images in folder
            image_count = len(find_images_in_directory(
                folder_path, 
                recursive=self.recursive.get()
            ))
            
            if image_count > 0:
                self.log_message(f"Found {image_count} images in folder")
            else:
                self.log_message("No valid images found in folder")
    
    def select_output_folder(self):
        """Open folder dialog to select output folder."""
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_path.set(folder_path)
            self.log_message(f"Selected output folder: {folder_path}")
    
    def update_preview(self, image_path):
        """Update the image preview canvas.
        
        Args:
            image_path (str): Path to image file to preview
        """
        if not image_path or not os.path.isfile(image_path):
            # Clear preview
            self.preview_canvas.delete("all")
            self.preview_image = None
            return
        
        try:
            # Open and resize image for preview
            img = Image.open(image_path)
            
            # Calculate resize dimensions to fit canvas
            canvas_width = self.preview_canvas.winfo_width() or 300
            canvas_height = self.preview_canvas.winfo_height() or 300
            
            # Resize image to fit canvas while maintaining aspect ratio
            width, height = img.size
            ratio = min(canvas_width / width, canvas_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for display
            photo_img = ImageTk.PhotoImage(img)
            
            # Clear previous image and display new one
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                canvas_width // 2, canvas_height // 2, 
                image=photo_img, anchor=tk.CENTER
            )
            
            # Keep a reference to prevent garbage collection
            self.preview_image = photo_img
            
            self.log_message(f"Loaded preview: {os.path.basename(image_path)}")
        except Exception as e:
            self.log_message(f"Error loading preview: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        about_text = f"""Color Palette Extractor v{__version__}

A tool to extract color palettes from images and generate harmonies.

Copyright (c) 2024 Michail Semoglou
Licensed under the MIT License

Project website: https://github.com/MichailSemoglou/color-palette-extractor
"""
        messagebox.showinfo("About", about_text)
    
    def start_processing(self):
        """Start processing images."""
        if self.processing:
            messagebox.showinfo("Processing in Progress", "Please wait for the current process to complete.")
            return
        
        input_path = self.input_path.get()
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or folder.")
            return
        
        output_path = self.output_path.get()
        if not output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        
        if not self.generate_pdf.get() and not self.generate_text.get():
            messagebox.showerror("Error", "Please select at least one output format (PDF or Text).")
            return
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Update configuration
        self.config_manager.set('num_colors', self.num_colors.get())
        self.config_manager.set('output_dir', output_path)
        self.config_manager.set('use_cache', self.use_cache.get())
        self.config_manager.set('generate_pdf', self.generate_pdf.get())
        self.config_manager.set('generate_text', self.generate_text.get())
        self.config_manager.save_config()
        
        # Start processing in a separate thread
        self.processing = True
        self.status_var.set("Processing...")
        threading.Thread(target=self.process_task, daemon=True).start()
    
    def process_task(self):
        """Process task in a separate thread."""
        try:
            # Reset progress bar
            self.progress_bar['value'] = 0
            self.root.update_idletasks()
            
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            num_colors = self.num_colors.get()
            recursive = self.recursive.get()
            use_cache = self.use_cache.get()
            generate_pdf = self.generate_pdf.get()
            generate_text = self.generate_text.get()
            
            self.log_message("Starting processing...")
            
            # Check if input is a file or directory
            if os.path.isfile(input_path):
                # Process single file
                self.log_message(f"Processing file: {os.path.basename(input_path)}")
                
                # Validate image
                if not is_valid_image(input_path):
                    raise ValueError(f"Not a valid image file: {input_path}")
                
                # Process the image
                result = process_images(
                    [input_path],
                    num_colors=num_colors,
                    output_dir=output_path,
                    generate_pdf=generate_pdf,
                    generate_text=generate_text,
                    use_cache=use_cache,
                    max_workers=1  # No parallelism for single image
                )
                
                # Update progress bar
                self.progress_bar['value'] = 100
                self.root.update_idletasks()
                
                # Check result
                if result['successful'] == 0:
                    error = result['results'][0].get('error', 'Unknown error')
                    raise ValueError(f"Failed to process image: {error}")
                
                # Log output files
                output_files = result['results'][0]['output_files']
                if output_files:
                    self.log_message("Output files:")
                    for file_path in output_files:
                        self.log_message(f"  {file_path}")
                
                processing_time = result['processing_time']
                self.log_message(f"Processing completed in {processing_time:.2f} seconds")
                
            else:
                # Process directory
                self.log_message(f"Processing directory: {input_path}")
                
                if not os.path.isdir(input_path):
                    raise ValueError(f"Directory not found: {input_path}")
                
                # Find images
                image_paths = find_images_in_directory(input_path, recursive=recursive)
                
                if not image_paths:
                    raise ValueError(f"No valid images found in directory: {input_path}")
                
                self.log_message(f"Found {len(image_paths)} images to process")
                
                # Process images
                result = process_images(
                    image_paths,
                    num_colors=num_colors,
                    output_dir=output_path,
                    generate_pdf=generate_pdf,
                    generate_text=generate_text,
                    use_cache=use_cache
                )
                
                # Update progress bar
                self.progress_bar['value'] = 100
                self.root.update_idletasks()
                
                # Log results
                successful = result['successful']
                failed = result['failed']
                processing_time = result['processing_time']
                
                self.log_message(f"Processed {len(image_paths)} images in {processing_time:.2f} seconds")
                self.log_message(f"Successful: {successful}, Failed: {failed}")
                
                if failed > 0:
                    self.log_message("Failed images:")
                    for r in result['results']:
                        if not r['success']:
                            self.log_message(f"  {os.path.basename(r['image_path'])}: {r.get('error', 'Unknown error')}")
            
            # Show success message
            messagebox.showinfo("Processing Complete", 
                               f"Processing completed successfully in {processing_time:.2f} seconds.")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.status_var.set("Ready")

def run_gui():
    """Run the GUI application."""
    root = tk.Tk()
    app = ColorPaletteExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
