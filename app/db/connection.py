"""
This module handles the creation and management of a PostgreSQL connection pool using psycopg2.
It provides functions to get, release, and close database connections from the pool.
"""

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

print(pool)

# Load environment variables from the .env file
load_dotenv()

# Create a connection pool for database connections
db_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    20,  # minconn, maxconn
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)


def get_db_connection():
    """Get a connection from the pool."""
    try:
        conn = db_pool.getconn()
        if conn is None:
            print("Unable to get a connection from the pool.")
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Error getting connection from pool: {e}")
        return None


def close_db_connection(conn):
    """Release the connection back to the pool."""
    try:
        if conn:
            db_pool.putconn(conn)
        else:
            print("Connection is None, cannot release.")
    except psycopg2.DatabaseError as e:
        print(f"Error releasing connection back to pool: {e}")


def close_pool():
    """Close all connections in the pool."""
    try:
        db_pool.closeall()
    except psycopg2.DatabaseError as e:
        print(f"Error closing the connection pool: {e}")
