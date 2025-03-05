"""
Configuration settings and constants for CV Analyzer.
"""

import os
import logging
import warnings
import google.cloud.logging
import chromadb
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv(override=True)

# API Keys and model settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

# Application paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DOCS_FOLDER = os.path.join(BASE_DIR, "docs")
LOGO_PATH = os.path.join(ASSETS_DIR, "cyborg.png")

def setup_logging():
    """Configure logging for the application"""
    # Set up Google Cloud Logging
    try:
        client = google.cloud.logging.Client()
        client.setup_logging()
    except Exception as e:
        # Fall back to standard logging if GCP logging fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.warning(f"Failed to set up Google Cloud Logging: {e}")
    
    logging.info("Starting CV Analysis Application...")
    
    # Initialize ChromaDB
    try:
        chromadb.api.client.SharedSystemClient.clear_system_cache()
    except Exception as e:
        logging.warning(f"Failed to clear ChromaDB cache: {e}")
