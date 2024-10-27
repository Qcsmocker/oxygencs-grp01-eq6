from datetime import datetime
import pytest
from app.db.connection import get_db_connection
from app.queries.sensor_data import insert_sensor_data


@pytest.fixture(scope="module")
def db_connection():
    # Setup database connection
    connection = get_db_connection()
    yield connection
    connection.close()


def test_sensor_data_insertion(db_connection):
    cursor = db_connection.cursor()

    # Step 1: Create a sample sensor event instance
    sensor_timestamp = datetime.now()
    sensor_temperature = 999.0

    # Step 2: Insert sensor data into the database
    insert_sensor_data(cursor, sensor_timestamp, sensor_temperature)
    db_connection.commit()

    # Step 3: Check if the sensor data was inserted
    cursor.execute(
        "SELECT COUNT(*) FROM sensor_events WHERE timestamp = %s AND temperature = %s",
        (sensor_timestamp, sensor_temperature),
    )
    result = cursor.fetchone()[0]

    assert result == 1, "Sensor data not inserted into the database."

    # Step 4: Optionally verify that the inserted data matches what was sent
    cursor.execute(
        "SELECT * FROM sensor_events WHERE timestamp = %s", (sensor_timestamp,)
    )
    sensor_record = cursor.fetchone()
    assert sensor_record is not None, "No sensor record found in the database."
    assert sensor_record[1] == sensor_temperature, "Sensor temperature does not match."
