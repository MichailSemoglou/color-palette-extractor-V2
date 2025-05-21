#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF report generation for the Color Palette Extractor 2.0
"""

import os
import logging
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

from color_palette_extractor.harmonies import is_dark
from .. import FONTS_DIR

logger = logging.getLogger(__name__)

# Register fonts
try:
    pdfmetrics.registerFont(TTFont('Inter-Bold', os.path.join(FONTS_DIR, 'Inter-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Inter-Regular', os.path.join(FONTS_DIR, 'Inter-Regular.ttf')))
    FONTS_REGISTERED = True
except:
    logger.warning("Unable to register Inter fonts. Using default fonts instead.")
    FONTS_REGISTERED = False

def save_palette_to_pdf(color_palette, harmonies, filename="color_palette.pdf", image_filename="", emotional_analysis=None, config=None):
    """Save the color palette and harmonies to a PDF file.
    
    Args:
        color_palette (list): List of color tuples from extract_color_palette
        harmonies (dict): Dictionary of color harmonies from get_harmonies
        filename (str): Output PDF filename
        image_filename (str): Original image filename for display
        emotional_analysis (dict, optional): Emotional analysis results
        config (dict, optional): Configuration options
            - page_size: PDF page size (default: A4)
            - margin: Margin in points (default: 36, 0.5 inch)
            - show_original_image: Whether to show the original image (default: True)
            - image_width: Width of the image in points (default: 216, 3 inches)
    
    Returns:
        str: Path to the created PDF file
    """
    # Apply default configuration
    if config is None:
        config = {}
    
    page_size = config.get('page_size', 'A4')
    margin = config.get('margin', 0.5 * inch)
    show_original_image = config.get('show_original_image', True)
    image_width = config.get('image_width', 3 * inch)
    
    # Create fonts and styles
    if FONTS_REGISTERED:
        title_font = 'Inter-Bold'
        body_font = 'Inter-Regular'
    else:
        title_font = 'Helvetica-Bold'
        body_font = 'Helvetica'
    
    # Create the document
    if page_size == 'A4':
        doc_page_size = A4
    else:
        # Default to A4 if page size is not recognized
        doc_page_size = A4
    
    doc = SimpleDocTemplate(filename, pagesize=doc_page_size, 
                           topMargin=margin, bottomMargin=margin,
                           leftMargin=margin, rightMargin=margin)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontName=title_font, fontSize=18, 
                                leading=20, alignment=TA_LEFT, spaceAfter=10)
    heading_style = ParagraphStyle(name='Heading2', fontName=title_font, fontSize=14, 
                                 leading=16, alignment=TA_LEFT, spaceBefore=16, spaceAfter=8)
    subheading_style = ParagraphStyle(name='Heading3', fontName=title_font, fontSize=12, 
                                    leading=14, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6)
    normal_style = ParagraphStyle(name='Normal', fontName=body_font, fontSize=10,
                                 leading=12, alignment=TA_LEFT, spaceBefore=6, spaceAfter=6)
    color_name_style = ParagraphStyle(name='ColorName', fontName=title_font, fontSize=11,
                                    leading=13, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4)
    
    # Title
    title = f"Color Palette and Harmonies"
    if image_filename:
        title += f" for {os.path.basename(image_filename)}"
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Add the original image if requested
    if show_original_image and image_filename and os.path.exists(image_filename):
        try:
            img = PILImage.open(image_filename)
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            
            # Calculate height based on aspect ratio
            display_width = image_width
            display_height = display_width * aspect

            elements.append(ReportLabImage(image_filename, width=display_width, height=display_height))
            elements.append(Spacer(1, 0.2*inch))
        except Exception as e:
            logger.error(f"Error adding image to PDF: {str(e)}")

    # Add color palette (in two rows)
    elements.append(Paragraph("Original Color Palette", heading_style))
    
    # Split palette into rows of 6 colors each
    palette_rows = []
    row = []
    for i, color in enumerate(color_palette):
        row.append(color[0])  # Add hex color
        if (i + 1) % 6 == 0 or i == len(color_palette) - 1:
            palette_rows.append(row)
            row = []
    
    # Create palette table
    palette_table = Table(palette_rows, colWidths=60, rowHeights=60)
    
    palette_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), body_font),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ])
    
    # Set background color for each cell
    for row_idx, row in enumerate(palette_rows):
        for col_idx, hex_color in enumerate(row):
            palette_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor(hex_color))
            text_color = colors.white if is_dark(hex_color) else colors.black
            palette_style.add('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), text_color)
    
    palette_table.setStyle(palette_style)
    elements.append(palette_table)

    # Add emotional analysis if available
    if emotional_analysis:
        elements.append(PageBreak())
        elements.append(Paragraph("Emotional Color Analysis", heading_style))
        
        # Add overall analysis
        elements.append(Paragraph("Overall Palette Impact", subheading_style))
        
        # Dominant emotions
        if "overall" in emotional_analysis and "dominant_emotions" in emotional_analysis["overall"]:
            emotions_text = "Dominant Emotions: " + ", ".join(emotional_analysis["overall"]["dominant_emotions"])
            elements.append(Paragraph(emotions_text, normal_style))
        
        # Harmony analysis
        if "overall" in emotional_analysis and "harmony_analysis" in emotional_analysis["overall"]:
            harmony_text = "Harmony Analysis: " + emotional_analysis["overall"]["harmony_analysis"]
            elements.append(Paragraph(harmony_text, normal_style))
        
        # Brand recommendations
        if "overall" in emotional_analysis and "brand_recommendations" in emotional_analysis["overall"]:
            brand_text = "Brand Recommendations: " + emotional_analysis["overall"]["brand_recommendations"]
            elements.append(Paragraph(brand_text, normal_style))
        
        # Add individual color analysis
        if "colors" in emotional_analysis and emotional_analysis["colors"]:
            elements.append(Paragraph("Individual Color Emotions", subheading_style))
            
            # Use individual color blocks instead of a table
            for color_info in emotional_analysis["colors"]:
                hex_color = color_info.get("hex", "#FFFFFF")
                color_name = color_info.get("color_name", "").capitalize()
                emotions = ", ".join(color_info.get("emotions", []))
                associations = ", ".join(color_info.get("associations", []))
                brand_fit = ", ".join(color_info.get("brand_fit", []))
                
                # Create a colored box
                color_box_data = [[hex_color]]
                color_box = Table(color_box_data, colWidths=[60], rowHeights=[30])
                color_box.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                    ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(hex_color)),
                    ('TEXTCOLOR', (0, 0), (0, 0), colors.white if is_dark(hex_color) else colors.black),
                    ('FONTNAME', (0, 0), (0, 0), body_font),
                    ('FONTSIZE', (0, 0), (0, 0), 8),
                    ('BOX', (0, 0), (0, 0), 1, colors.black),
                ]))
                
                elements.append(Spacer(1, 0.1*inch))
                elements.append(color_box)
                elements.append(Paragraph(f"<b>{color_name} ({hex_color})</b>", color_name_style))
                elements.append(Paragraph(f"<b>Emotional Response:</b> {emotions}", normal_style))
                elements.append(Paragraph(f"<b>Associations:</b> {associations}", normal_style))
                elements.append(Paragraph(f"<b>Brand Fit:</b> {brand_fit}", normal_style))

    # Add harmonies
    harmony_pages = ["Original Color Palette"]  # Start with the palette page
    # Add emotional analysis page if applicable
    if emotional_analysis:
        harmony_pages.append("Emotional Analysis")
        
    for harmony_type, harmony_sets in harmonies.items():
        # Add a page break before "Complementary Harmonies"
        if harmony_type == "complementary":
            elements.append(PageBreak())

        # Capitalize harmony type for display
        display_harmony_type = harmony_type.capitalize()
        elements.append(Paragraph(f"{display_harmony_type} Harmonies", heading_style))
        harmony_pages.append(display_harmony_type)
        
        for idx, harmony_set in enumerate(harmony_sets):
            harmony_data = [list(harmony_set.values())]
            harmony_table = Table(harmony_data, colWidths=60, rowHeights=60)
            
            harmony_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), body_font),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
            ])
            
            for i, color_hex in enumerate(harmony_set.values()):
                harmony_style.add('BACKGROUND', (i, 0), (i, 0), colors.HexColor(color_hex))
                text_color = colors.white if is_dark(color_hex) else colors.black
                harmony_style.add('TEXTCOLOR', (i, 0), (i, 0), text_color)
            
            harmony_table.setStyle(harmony_style)
            elements.append(harmony_table)

        # Add page break after each harmony type, except for the last one
        if harmony_type != list(harmonies.keys())[-1]:
            elements.append(PageBreak())

    # Function to add page numbers and header to each page
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        harmony_name = harmony_pages[min(page_num - 1, len(harmony_pages) - 1)]
        
        # Add header with file name and harmony type
        header_text = f"Page {page_num}"
        if image_filename:
            header_text += f" | Image: {os.path.basename(image_filename)}"
        header_text += f" | {harmony_name}"
        
        canvas.setFont(body_font, 8)
        canvas.drawString(margin, margin / 2, header_text)

    # Build the PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    logger.info(f"Saved PDF to {filename}")
    return filename
