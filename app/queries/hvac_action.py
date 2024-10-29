"""
This module provides database query functions related to HVAC actions.
"""

import psycopg2

from app.queries.data_models import HvacAction


def insert_hvac_action(cursor, hvac_action: HvacAction):
    """
    Insert HVAC action into the hvac_actions table.

    :param cursor: Database cursor object.
    :param hvac_action: An instance of HvacAction containing details about the action.
    """
    query = (
        "INSERT INTO hvac_actions (action_timestamp, action_type, temperature, "
        "sensor_event_id, response_details) VALUES (%s, %s, %s, %s, %s)"
    )
    try:
        cursor.execute(
            query,
            (
                hvac_action.action_timestamp,
                hvac_action.action_type,
                hvac_action.temperature,
                hvac_action.sensor_event_id,
                hvac_action.response_details,
            ),
        )
    except psycopg2.DatabaseError as e:
        print(f"Error inserting HVAC action: {e}")
