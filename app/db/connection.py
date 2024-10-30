"""
This module provides functions for database connection management.
"""

import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def get_db_connection():
    """Connect to the database using environment variables."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def close_db_connection(conn):
    """Close the database connection."""
    conn.close()
