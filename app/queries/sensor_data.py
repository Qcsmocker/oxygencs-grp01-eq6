def insert_sensor_data(
    cursor, timestamp, temperature
):
    """
    Insert sensor data into the sensor_events table.

    :param cursor: Database cursor object.
    :param timestamp: The time the sensor data was recorded.
    :param temperature: The temperature reading from the sensor.
    """
    query = """INSERT INTO sensor_events (timestamp, temperature, sensor_id, status) VALUES (%s, %s)"""
    cursor.execute(query, (timestamp, temperature))
