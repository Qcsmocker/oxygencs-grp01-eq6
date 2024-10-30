"""
Entry point to initialize and run the main application.
"""

import os
import sys

# Set PYTHONPATH to the project directory
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Import and run the main app code
from app.main import run_app  # pylint: disable=C0413

run_app()  # Call your main function
