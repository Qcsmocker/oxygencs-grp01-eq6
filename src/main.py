"""
Main application module for managing HVAC operations and sensor data handling.
"""

import logging
import json
import time
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder

class App:
    """Main application class for Oxygen CS."""

    def __init__(self):
        self._hub_connection = None
        self.ticks = 10

        # To be configured by your team
        self.host = None
        self.token = None
        self.t_max = None
        self.t_min = None
        self.database_url = None

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.host}/SensorHub?token={self.token}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature)
        except (KeyError, ValueError) as err:
            print(f"Error processing data: {err}")

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.t_max):
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.t_min):
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        response = requests.get(f"{self.host}/api/hvac/{self.token}/{action}/{self.ticks}")
        details = json.loads(response.text)
        print(details, flush=True)

    def save_event_to_database(self, _timestamp, _temperature):
        """Save sensor data into database."""
        pass  # To implement

if __name__ == "__main__":
    app = App()
    app.start()