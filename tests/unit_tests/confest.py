"""
This module provides shared fixtures for unit tests.
"""

import os
import sys
from dotenv import load_dotenv

# Set the project root as the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()  # Load .env variables
