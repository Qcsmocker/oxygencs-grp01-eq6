"""
Main application file for the Oxygen CS project.
Handles initialization, environment configurations, and the main loop for data processing.
"""

import os
import threading
import time
from dotenv import load_dotenv

from .api.hvac_control_api import send_action_to_hvac
from .api.sensor_hub_api import setup_sensor_hub
from .services.ci_metrics_service import CIMetricsCalculator
from .services.database_service import DatabaseService  # Place all imports here

# Set the PYTHONPATH
os.environ["PYTHONPATH"] = os.path.abspath(
    os.path.dirname(__file__)
)  # This sets the PYTHONPATH to the current directory.


class App:
    """Main application class for Oxygen CS."""

    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()
        self.config = {
            "host": os.getenv("HOST"),
            "token": os.getenv("TOKEN"),
            "t_max": float(os.getenv("T_MAX")) + 10,
            "t_min": float(os.getenv("T_MIN")),
            "ticks": 10,
        }
        self.ac_on = False
        self.heater_on = False
        self._hub_connection = None

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def run(self):
        """Initialize and start Oxygen CS."""
        # Start the CI Metrics calculation thread
        threading.Thread(target=self.schedule_metrics_update, daemon=True).start()

        # Start handling sensor data and HVAC actions
        self.handle_data_loop()

    def schedule_metrics_update(self):
        """Schedule the metrics calculation and update every minute."""
        while True:
            try:
                print("\nCalculating CI Metrics...")
                ci_metrics = CIMetricsCalculator.calculate_ci_metrics()
                if ci_metrics:
                    DatabaseService.store_ci_metrics(ci_metrics)
                print("CI Metrics updated successfully.")
            except (ConnectionError, ValueError) as e:
                print(f"Error calculating CI Metrics: {e}")

            time.sleep(60)  # Wait for 1 minute before the next update

    def handle_data_loop(self):
        """Main loop to handle sensor data and HVAC actions without delay."""
        print("Press CTRL+C to exit.")
        self._hub_connection = setup_sensor_hub(
            self.config["host"], self.config["token"], self.handle_sensor_data
        )
        self._hub_connection.start()
        while True:
            time.sleep(1)  # Adjust as needed for your sensor data frequency

    def handle_sensor_data(self, data):
        """Callback method to handle sensor data reception."""
        try:
            # Print the received raw sensor data
            print(f"\nRaw Sensor Data Received: {data}")

            # Extract timestamp and temperature
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])

            # Save sensor data to DB and get the sensor_event_id
            sensor_event_id = DatabaseService.store_sensor_data(
                {"timestamp": timestamp, "temperature": temperature}
            )

            # Determine and perform any necessary HVAC actions
            self.determine_hvac_action(temperature, sensor_event_id)

        except (KeyError, ValueError) as err:
            print(f"Error processing sensor data: {err}")

    def determine_hvac_action(self, temperature, sensor_event_id):
        """Determine and execute the appropriate HVAC action based on the temperature."""
        t_min = self.config["t_min"]
        t_max = self.config["t_max"]

        if temperature < t_min:
            if not self.heater_on:
                print(
                    f"Temperature {temperature} is below T_MIN: {t_min}. Turning on Heater."
                )
                self.perform_hvac_action("TurnOnHeater", temperature, sensor_event_id)
                self.heater_on = True
            if self.ac_on:
                print(f"Temperature {temperature} is below T_MIN. Turning off AC.")
                self.perform_hvac_action("TurnOffAc", temperature, sensor_event_id)
                self.ac_on = False
        elif temperature > t_max:
            if not self.ac_on:
                print(f"Temperature {temperature} exceeds T_MAX. Turning on AC.")
                self.perform_hvac_action("TurnOnAc", temperature, sensor_event_id)
                self.ac_on = True
            if self.heater_on:
                print(f"Temperature {temperature} exceeds T_MAX. Turning off Heater.")
                self.perform_hvac_action("TurnOffHeater", temperature, sensor_event_id)
                self.heater_on = False
        else:
            if self.ac_on:
                print(
                    f"Temperature {temperature} is within the acceptable range. Turning off AC."
                )
                self.perform_hvac_action("TurnOffAc", temperature, sensor_event_id)
                self.ac_on = False
            if self.heater_on:
                print(
                    f"Temperature {temperature} is within the acceptable range. Turning off Heater."
                )
                self.perform_hvac_action("TurnOffHeater", temperature, sensor_event_id)
                self.heater_on = False

    def perform_hvac_action(self, action_type, temperature, sensor_event_id):
        """Send the action to the HVAC system and save the action to the database."""
        try:
            # Send the action to the HVAC system
            response = send_action_to_hvac(
                self.config["host"],
                self.config["token"],
                action_type,
                self.config["ticks"],
            )

            print(f"Performing HVAC Action: {action_type}")

            # Store the HVAC action in the database
            DatabaseService.store_hvac_action(
                action_type, temperature, sensor_event_id, response
            )

        except (KeyError, ValueError) as e:
            print(f"Error performing HVAC action: {e}")


def run_app():
    """Initialize and run the main application."""
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        # Perform any cleanup if necessary
    finally:
        # Any final cleanup code goes here
        print("App has stopped.")


if __name__ == "__main__":
    run_app()
