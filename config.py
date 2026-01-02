# ============================================================================
# FILE: config.py
# Configuration settings for the application
# ============================================================================

import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).parent

# Data storage directories
DATA_DIR = BASE_DIR / "data"
EXPERIMENTS_DIR = DATA_DIR / "experiments"
EXPORTS_DIR = BASE_DIR / "exports"

# Create directories if they don't exist
EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Statistical settings
ALPHA_LEVEL = 0.05  # Significance level for chi-square test

# Export settings
DEFAULT_CHART_DPI = 300
DEFAULT_CHART_SIZE = (10, 6)

# Application metadata
APP_NAME = "Fruit Fly Genetics Tracker"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Jiya Gangwar"