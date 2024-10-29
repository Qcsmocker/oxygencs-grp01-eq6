"""
This module provides shared fixtures for integration tests.
"""

import pytest
from app.db.connection import get_db_connection, close_db_connection


@pytest.fixture(scope="module")
def db_test_connection():
    """Fixture to set up and tear down the database connection for tests."""
    connection = get_db_connection()
    yield connection
    close_db_connection(connection)
