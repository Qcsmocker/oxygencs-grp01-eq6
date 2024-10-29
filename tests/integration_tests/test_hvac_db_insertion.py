"""
Integration tests for verifying HVAC action insertion into the database.
"""

# pylint: disable=E0401
from datetime import datetime
from app.queries.data_models import HvacAction
from app.queries.hvac_action import insert_hvac_action
from app.queries.sensor_data import insert_sensor_data


def test_hvac_action_insertion(db_test_connection):
    """Test to insert an HVAC action into the database and verify its insertion."""
    cursor = db_test_connection.cursor()

    # Step 1: Insert a sample sensor event first
    sensor_timestamp = datetime.now()
    sensor_temperature = 20.0
    insert_sensor_data(cursor, sensor_timestamp, sensor_temperature)
    cursor.execute("SELECT LASTVAL();")
    sensor_event_id = cursor.fetchone()[0]

    # Step 2: Create a sample HVAC action instance
    action_timestamp = datetime.now()
    action_type = "TurnOnHeater"
    temperature = 22.5
    response_details = '{"Integration Test"}'

    hvac_action = HvacAction(
        action_timestamp=action_timestamp,
        action_type=action_type,
        temperature=temperature,
        sensor_event_id=sensor_event_id,
        response_details=response_details,
    )

    # Step 3: Insert HVAC action into the database
    insert_hvac_action(cursor, hvac_action)
    db_test_connection.commit()

    # Step 4: Check if the action was inserted
    cursor.execute(
        "SELECT COUNT(*) FROM hvac_actions WHERE action_timestamp = %s",
        (action_timestamp,),
    )
    result = cursor.fetchone()[0]

    assert result == 1, "HVAC action not inserted into the database."
