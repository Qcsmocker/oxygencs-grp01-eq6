"""
This module provides service functions for interacting with the database,
including storing sensor data, HVAC actions, and CI metrics.
"""

import json
import psycopg2
from app.db.connection import close_db_connection, get_db_connection
from app.queries.ci_metrics import insert_ci_metrics
from app.queries.data_models import HvacAction
from app.queries.hvac_action import insert_hvac_action
from app.queries.sensor_data import insert_sensor_data
from app.utils.datetime_utils import get_current_timestamp


class DatabaseService:
    """Service class for database operations related to sensor data,
    HVAC actions, and CI metrics."""

    @staticmethod
    def store_sensor_data(sensor_data):
        """Store sensor data in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_sensor_data(
                cursor, sensor_data["timestamp"], sensor_data["temperature"]
            )
            cursor.execute("SELECT LASTVAL();")
            sensor_event_id = cursor.fetchone()[0]
            conn.commit()
            return sensor_event_id
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print(f"Error inserting sensor data: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)

    @staticmethod
    def store_hvac_action(action_type, temperature, sensor_event_id, response_details):
        """Create and store an HVAC action in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Create the HvacAction object
            hvac_action = HvacAction(
                action_timestamp=get_current_timestamp(),
                action_type=action_type,
                temperature=temperature,
                sensor_event_id=sensor_event_id,
                response_details=json.dumps(response_details),
            )

            # Insert HvacAction into the database
            insert_hvac_action(cursor, hvac_action)
            conn.commit()
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print(f"Error inserting HVAC action: {e}")
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)

    @staticmethod
    def store_ci_metrics(ci_metrics):
        """Store CI metrics in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_ci_metrics(cursor, ci_metrics)
            cursor.execute("SELECT LASTVAL();")
            conn.commit()
            print("CI Metrics inserted successfully.")
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print(f"Error inserting CI Metrics data: {e}")
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)
