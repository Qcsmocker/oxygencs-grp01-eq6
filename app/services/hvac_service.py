import json
from app.api.hvac_control_api import send_action_to_hvac
from app.utils.datetime_utils import get_current_timestamp
from app.services.database_service import DatabaseService
from app.queries.data_models import HvacAction  # Ensure you have this import

class HvacService:
    @staticmethod
    def perform_hvac_action(host, token, action_type, temperature, sensor_event_id):
        """Send the action to the HVAC system and store it."""
        try:
            # Send the action to the HVAC system and get the response
            response_status, response_details = send_action_to_hvac(host, token, action_type, 10)

            # Convert response details to a clean JSON string
            response_details_json = json.dumps(response_details, indent=2)

            # Log the action in a readable format
            print(f"\nPerforming HVAC Action: {action_type}")

            # Create the HvacAction object to insert into the database
            hvac_action = HvacAction(
                action_timestamp=get_current_timestamp(),
                action_type=action_type,
                temperature=temperature,
                sensor_event_id=sensor_event_id,
                response_details=response_details_json,
            )

            # Store the HVAC action in the database
            DatabaseService.store_all_data(hvac_action=hvac_action)
        except Exception as e:
            print(f"Error performing HVAC action: {e}")
