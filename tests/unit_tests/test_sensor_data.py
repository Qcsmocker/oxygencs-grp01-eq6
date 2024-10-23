import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app.queries.sensor_data import insert_sensor_data


class TestSensorEventInsertion(unittest.TestCase):
    @patch("db.connection.get_db_connection")
    @patch("db.connection.close_db_connection")
    def test_sensor_event_insertion(
        self, mock_close_db_connection, mock_get_db_connection
    ):
        """Test for successful insertion into sensor_events table."""

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Example data for sensor event
        timestamp = datetime.now(timezone.utc)
        temperature = 22.5
        sensor_id = "sensor-001"
        status = "OK"
        other_data = None

        # Execute the sensor event insertion
        insert_sensor_data(
            mock_cursor, timestamp, temperature, sensor_id, status, other_data
        )

        # Check that the cursor executed the query
        mock_cursor.execute.assert_called_once()

        # Get the actual executed query
        actual_query = (
            mock_cursor.execute.call_args[0][0].replace("\n", "").strip()
        )  # Remove newlines and strip whitespace

        # Define the expected query
        expected_query = "INSERT INTO sensor_events (timestamp, temperature, sensor_id, status, other_data) VALUES (%s, %s, %s, %s, %s)"

        # Normalize the actual query by removing excessive whitespace
        actual_query = " ".join(actual_query.split())

        # Assert that the actual query matches the expected query
        self.assertEqual(actual_query, expected_query)


if __name__ == "__main__":
    unittest.main()
