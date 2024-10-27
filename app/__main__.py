import sys
import os

# Set PYTHONPATH to the project directory
project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Adjust as needed for your structure
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Import and run your main app code
from app.main import run_app  # Adjust the import based on your structure

run_app()  # Call your main function
