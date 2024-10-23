import unittest
from signalrcore.hub_connection_builder import HubConnectionBuilder
from dotenv import load_dotenv
import os
import time


class SensorHubConnectionTest(unittest.TestCase):
    """Test connection to the Sensor Hub."""

    def setUp(self):
        """Load environment variables and setup sensor hub connection."""
        load_dotenv()
        self.host = os.getenv("HOST")
        self.token = os.getenv("TOKEN")
        self._hub_connection = None

        # Check that necessary environment variables are available
        if not self.host or not self.token:
            self.fail("Environment variables HOST and TOKEN must be set")

    def test_sensor_hub_connection(self):
        """Test if connection to the sensor hub is successful."""
        # Configure the hub connection
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.host}/SensorHub?token={self.token}")
            .build()
        )

        # Set up the connection status flags
        self.connection_opened = False
        self.connection_closed = False

        # Define the event handlers
        self._hub_connection.on_open(lambda: self.set_flag("connection_opened", True))
        self._hub_connection.on_close(lambda: self.set_flag("connection_closed", True))

        # Start the connection
        self._hub_connection.start()
        time.sleep(2)  # Give it time to connect

        # Assert the connection was opened successfully
        self.assertTrue(
            self.connection_opened, "Failed to open connection to Sensor Hub"
        )

        # Stop the connection and assert it closed successfully
        self._hub_connection.stop()
        self.assertTrue(
            self.connection_closed, "Failed to close connection to Sensor Hub"
        )

    def set_flag(self, flag_name, value):
        """Helper function to set connection flags."""
        setattr(self, flag_name, value)

    def tearDown(self):
        """Stop the hub connection if it's still active."""
        if self._hub_connection:
            self._hub_connection.stop()


if __name__ == "__main__":
    unittest.main()
