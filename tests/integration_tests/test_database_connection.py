import unittest
from app.db.connection import get_db_connection, close_db_connection


class DatabaseConnectionTest(unittest.TestCase):
    """Test connection to the database."""

    def test_database_connection(self):
        """Test if connection to the database is successful."""
        try:
            # Try to open a connection
            conn = get_db_connection()
            cursor = conn.cursor()

            # Test if we can execute a simple query (e.g., fetching the current date)
            cursor.execute("SELECT NOW();")
            result = cursor.fetchone()

            # Assert that the query result is not None
            self.assertIsNotNone(result, "Failed to execute test query on the database")
            print(f"Database connected. Current time: {result[0]}")

            # Clean up
            cursor.close()
            close_db_connection(conn)

        except Exception as e:
            self.fail(f"Failed to connect to the database: {str(e)}")


if __name__ == "__main__":
    unittest.main()
