"""
Integration tests for verifying sensor data insertion into the database.
"""

# pylint: disable=E0401
from datetime import datetime
from app.queries.sensor_data import insert_sensor_data


def test_sensor_data_insertion(db_test_connection):
    """Test to insert sensor data into the database and verify its insertion."""
    cursor = db_test_connection.cursor()

    # Step 1: Create a sample sensor event instance
    sensor_timestamp = datetime.now()
    sensor_temperature = 999.0

    # Step 2: Insert sensor data into the database
    insert_sensor_data(cursor, sensor_timestamp, sensor_temperature)
    db_test_connection.commit()

    # Step 3: Check if the sensor data was inserted
    cursor.execute(
        "SELECT COUNT(*) FROM sensor_events WHERE timestamp = %s AND temperature = %s",
        (sensor_timestamp, sensor_temperature),
    )
    result = cursor.fetchone()[0]

    assert result == 1, "Sensor data not inserted into the database."
