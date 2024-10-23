def insert_sensor_data(
    cursor, timestamp, temperature, sensor_id="sensor-001", status="OK", other_data=None
):
    """
    Insert sensor data into the sensor_events table.

    :param cursor: Database cursor object.
    :param timestamp: The time the sensor data was recorded.
    :param temperature: The temperature reading from the sensor.
    :param sensor_id: The ID of the sensor that generated the data (default: 'sensor-001').
    :param status: The status of the sensor data (e.g., 'OK' or 'ERROR').
    :param other_data: Any additional data coming from the sensor (optional).
    """
    query = """INSERT INTO sensor_events (timestamp, temperature, sensor_id, status, other_data) VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (timestamp, temperature, sensor_id, status, other_data))
