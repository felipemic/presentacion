"""
Utility functions for CV Analyzer.
"""

import os
import io
import shutil
import logging
from typing import List

import fitz
from PIL import Image

from config import DOCS_FOLDER

def setup_folders():
    """Ensure necessary folders exist"""
    if not os.path.exists(DOCS_FOLDER):
        os.makedirs(DOCS_FOLDER)
        logging.info(f"Created folder: {DOCS_FOLDER}")

def delete_docs(folder):
    """
    Clean up document folder
    
    Args:
        folder (str): Path to the folder to clean
    """
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
            os.makedirs(folder)
            logging.info(f"Cleaned up folder: {folder}")
        except Exception as e:
            logging.error(f"Error cleaning up folder {folder}: {e}")

def get_pdf_previews(pdf_path: str, scale: float = 2.0) -> List[Image.Image]:
    """
    Generate preview images for all pages in a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        scale: Image scale factor for resolution adjustment
        
    Returns:
        List of PIL Image objects
    """
    try:
        doc = fitz.open(pdf_path)
        previews = []
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            img = Image.open(io.BytesIO(pix.tobytes()))
            previews.append(img)
        logging.info(f"Generated {len(previews)} preview images for {pdf_path}")
        return previews
    except Exception as e:
        logging.error(f"Error generating PDF previews for {pdf_path}: {e}")
        return []
