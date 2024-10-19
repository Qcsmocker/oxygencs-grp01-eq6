def insert_hvac_action(cursor, action_timestamp, action_type, temperature, sensor_event_id, response_status, response_details):
    """
    Insert HVAC action into the hvac_actions table.

    :param cursor: Database cursor object.
    :param action_timestamp: Timestamp of when the action was taken.
    :param action_type: The type of HVAC action (e.g., TurnOnAc).
    :param temperature: The temperature reading at the time of action.
    :param sensor_event_id: The ID of the sensor event associated with this action.
    :param response_status: The status of the HVAC system response.
    :param response_details: Any details regarding the response (e.g., API response).
    """
    query = """INSERT INTO hvac_actions (action_timestamp, action_type, temperature, sensor_event_id, response_status, response_details) VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (action_timestamp, action_type, temperature, sensor_event_id, response_status, response_details))
