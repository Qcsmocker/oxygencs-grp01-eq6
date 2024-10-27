from datetime import datetime
import pytest
from app.db.connection import get_db_connection
from app.queries.data_models import HvacAction
from app.queries.hvac_action import insert_hvac_action
from app.queries.sensor_data import insert_sensor_data

@pytest.fixture(scope="module")
def db_connection():
    # Setup database connection
    connection = get_db_connection()
    yield connection
    connection.close()

def test_hvac_action_insertion(db_connection):
    cursor = db_connection.cursor()

    # Step 1: Insert a sample sensor event first
    sensor_timestamp = datetime.now()
    sensor_temperature = 20.0
    insert_sensor_data(cursor, sensor_timestamp, sensor_temperature)
    cursor.execute("SELECT LASTVAL();")
    sensor_event_id = cursor.fetchone()[0]

    # Debugging: Verify sensor event was inserted
    print(f"Inserted Sensor Event ID: {sensor_event_id}")

    # Step 2: Create a sample HVAC action instance
    action_timestamp = datetime.now()
    action_type = "TurnOnHeater"
    temperature = 22.5
    response_details = '{"Integration Test"}'

    hvac_action = HvacAction(
        action_timestamp=action_timestamp,
        action_type=action_type,
        temperature=temperature,
        sensor_event_id=sensor_event_id,  # Use the valid sensor_event_id
        response_details=response_details
    )

    # Step 3: Insert HVAC action into the database
    insert_hvac_action(cursor, hvac_action)
    db_connection.commit()

    # Step 4: Check if the action was inserted
    cursor.execute("SELECT COUNT(*) FROM hvac_actions WHERE action_type = %s", (action_type,))
    result = cursor.fetchone()[0]

    assert result == 1, "HVAC action not inserted into the database."

    # Optional: Verify the action details in the database if needed
    cursor.execute("SELECT * FROM hvac_actions WHERE action_type = %s", (action_type,))
    action_record = cursor.fetchone()
    assert action_record is not None, "No action record found in the database."
    assert action_record[1] == action_timestamp, "Action timestamp does not match."

