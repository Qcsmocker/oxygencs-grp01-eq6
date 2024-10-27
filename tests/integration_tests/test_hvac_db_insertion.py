import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


import unittest
import json
from app.db.connection import get_db_connection, close_db_connection
from app.main import App  # Correct import for the App class
from app.utils.datetime_utils import format_timestamp


class TestHVACDBInsertion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Establish a real connection to the database
        cls.connection = get_db_connection()
        cls.cursor = cls.connection.cursor()

    def test_hvac_data_insertion(self):
        # Initialize the app
        app = App()

        # Sample sensor data with formatted timestamp
        timestamp = (
            format_timestamp()
        )  # Use the format_timestamp function from helpers.py
        temperature = 999.9  # Use a distinct temperature to mark this as test data
        sensor_event_id = app.save_sensor_event_to_db(timestamp, temperature)

        # Assert sensor_event_id was created
        self.assertIsNotNone(
            sensor_event_id, "Failed to insert sensor event into the database"
        )

        # Simulate an HVAC action based on the sensor data
        action_type = "TurnOnAc" if temperature > app.t_max else "TurnOffAc"

        # Create a response indicating this is test data
        test_response_details = {
            "status": "Test",
            "description": "This is a test data entry",
        }
        response_details_json = json.dumps(test_response_details)

        # Execute HVAC action with test data
        action_timestamp = format_timestamp()  # Use the formatted timestamp
        app.execute_hvac_action(action_type, temperature, sensor_event_id)

        # Verify the HVAC data was inserted into the database with the test label
        self.cursor.execute(
            """
            SELECT action_type, temperature, sensor_event_id, response_details
            FROM hvac_actions
            WHERE response_details->>'status' = 'Test';
        """
        )
        result = self.cursor.fetchone()

        # Ensure that the data exists and matches the expected test values
        self.assertIsNotNone(result, "No test data found in the database.")
        self.assertIn("Test", result[3], "Inserted data is not marked as test data.")
        self.assertEqual(
            result[1], 999.9, "The temperature does not match the test data value."
        )

    @classmethod
    def tearDownClass(cls):
        # Close the database connection after all tests are complete
        cls.cursor.close()
        close_db_connection(cls.connection)


if __name__ == "__main__":
    unittest.main()
