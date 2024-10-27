"""
This module provides database query functions for sensor data.
"""

from app.queries.data_models import SensorData  # Updated import


def insert_sensor_data(cursor, timestamp, temperature):
    """
    Insert sensor data into the database.

    :param cursor: Database cursor object.
    :param timestamp: Timestamp of the sensor data.
    :param temperature: Temperature value recorded by the sensor.
    """
    cursor.execute(
        """
        INSERT INTO sensor_events (timestamp, temperature)
        VALUES (%s, %s)
        """,
        (timestamp, temperature),
    )
