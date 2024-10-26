import json
import threading
import time
from datetime import datetime, timezone
from app.api.sensor_hub_api import (
    setup_sensor_hub,
)  # Ensure the correct import path for setup_sensor_hub
from app.api.hvac_control_api import send_action_to_hvac
from app.db.connection import get_db_connection, close_db_connection
from app.queries.sensor_data import insert_sensor_data
from app.queries.hvac_action import insert_hvac_action
import os
from dotenv import load_dotenv

class App:
    """Main application class for Oxygen CS."""

    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()
        self.host = os.getenv("HOST")
        self.token = os.getenv("TOKEN")
        self.t_max = float(os.getenv("T_MAX"))
        self.t_min = float(os.getenv("T_MIN"))
        self.ticks = 10
        self.ac_on = False
        self.heater_on = False
        self._hub_connection = None

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self._hub_connection = setup_sensor_hub(
            self.host, self.token, self.on_sensor_data_received
        )
        self._hub_connection.start()

        # Start a thread to calculate metrics every minute
        threading.Thread(target=self.schedule_metrics_collection).start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def schedule_metrics_collection(self):
        """Schedule the metrics calculation every minute."""
        while True:
            self.calculate_and_insert_metrics()
            time.sleep(60)  # Wait for 1 minute before the next collection

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data reception."""
        try:
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            sensor_event_id = self.save_sensor_event_to_db(timestamp, temperature)
            self.take_action(temperature, sensor_event_id)
        except (KeyError, ValueError) as err:
            print(f"Error processing sensor data: {err}")

    def save_sensor_event_to_db(self, timestamp, temperature):
        """Insert sensor data and retrieve sensor_event_id."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_sensor_data(cursor, timestamp, temperature)  # Corrected to match query
            conn.commit()
            cursor.execute("SELECT LASTVAL();")  # Get the last inserted sensor_event_id
            sensor_event_id = cursor.fetchone()[0]
            cursor.close()
            close_db_connection(conn)
            return sensor_event_id
        except Exception as e:
            print(f"Error saving sensor data: {e}")
            return None


    def take_action(self, temperature, sensor_event_id):
        """Determine and execute the appropriate HVAC action."""
        if temperature < self.t_min:
            if not self.heater_on:
                print(
                    f"Temperature {temperature} is below T_MIN: {self.t_min}. Turning on Heater."
                )
                self.execute_hvac_action("TurnOnHeater", temperature, sensor_event_id)
                self.heater_on = True
            if self.ac_on:
                print(f"Temperature {temperature} is below T_MIN. Turning off AC.")
                self.execute_hvac_action("TurnOffAc", temperature, sensor_event_id)
                self.ac_on = False
        elif temperature > self.t_max:
            if not self.ac_on:
                print(f"Temperature {temperature} exceeds T_MAX. Turning on AC.")
                self.execute_hvac_action("TurnOnAc", temperature, sensor_event_id)
                self.ac_on = True
            if self.heater_on:
                print(f"Temperature {temperature} exceeds T_MAX. Turning off Heater.")
                self.execute_hvac_action("TurnOffHeater", temperature, sensor_event_id)
                self.heater_on = False
        else:
            if self.ac_on:
                print(
                    f"Temperature {temperature} is within the acceptable range. Turning off AC."
                )
                self.execute_hvac_action("TurnOffAc", temperature, sensor_event_id)
                self.ac_on = False
            if self.heater_on:
                print(
                    f"Temperature {temperature} is within the acceptable range. Turning off Heater."
                )
                self.execute_hvac_action("TurnOffHeater", temperature, sensor_event_id)
                self.heater_on = False

    def execute_hvac_action(self, action_type, temperature, sensor_event_id):
        """Send the action to the HVAC system and save the action to the database."""
        try:
            # Send the action to the HVAC system and get the response
            response_details = send_action_to_hvac(
                self.host, self.token, action_type, self.ticks
            )

            # Convert the response_details dict to a JSON string
            response_details_json = json.dumps(response_details)

            action_timestamp = datetime.now(timezone.utc)
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the HVAC action into the database
            insert_hvac_action(
                cursor,
                action_timestamp,
                action_type,
                temperature,
                sensor_event_id,
                response_details_json
            )

            conn.commit()
            cursor.close()
            close_db_connection(conn)

        except Exception as e:
            print(f"Error executing HVAC action: {e}")

    def calculate_and_insert_metrics(self):
        """Calculate and insert integration metrics into the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Calculate the number of sensor events per minute
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM sensor_events
                WHERE timestamp >= NOW() - INTERVAL '1 minute'
            """
            )
            sensor_events_per_minute = cursor.fetchone()[0]

            # Calculate the number of HVAC actions per minute
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM hvac_actions
                WHERE action_timestamp >= NOW() - INTERVAL '1 minute'
            """
            )
            hvac_actions_per_minute = cursor.fetchone()[0]

            # Calculate the average sensor temperature for the last minute
            cursor.execute(
                """
                SELECT AVG(temperature)
                FROM sensor_events
                WHERE timestamp >= NOW() - INTERVAL '1 minute'
            """
            )
            average_sensor_temperature = (
                cursor.fetchone()[0] or 0
            )  # default to 0 if no data

            # Calculate the average HVAC response time for the last minute
            cursor.execute(
                """
                SELECT AVG(EXTRACT(EPOCH FROM (action_timestamp - sensor_events.timestamp)))
                FROM hvac_actions
                JOIN sensor_events ON hvac_actions.sensor_event_id = sensor_events.id
                WHERE hvac_actions.action_timestamp >= NOW() - INTERVAL '1 minute'
            """
            )
            average_hvac_response_time = (
                cursor.fetchone()[0] or 0
            )  # default to 0 if no data

            # Insert the metrics into the integration_metrics table
            cursor.execute(
                """
                INSERT INTO integration_metrics (
                    timestamp,
                    sensor_events_per_minute,
                    hvac_actions_per_minute,
                    average_sensor_temperature,
                    average_hvac_response_time
                ) VALUES (%s, %s, %s, %s, %s)
            """,
                (
                    datetime.now(),
                    sensor_events_per_minute,
                    hvac_actions_per_minute,
                    average_sensor_temperature,
                    average_hvac_response_time,
                ),
            )

            conn.commit()
            cursor.close()
            close_db_connection(conn)

            print(
                f"Metrics inserted: {sensor_events_per_minute} sensor events, {hvac_actions_per_minute} HVAC actions, {average_sensor_temperature:.2f}°C avg temp, {average_hvac_response_time:.2f}s avg response time."
            )

        except Exception as e:
            print(f"Error calculating and inserting metrics: {e}")


if __name__ == "__main__":
    app = App()
    app.start()
