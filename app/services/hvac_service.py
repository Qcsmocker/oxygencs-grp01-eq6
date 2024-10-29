"""
HVAC service for managing actions related to the HVAC system.
"""

# pylint: disable=R0903  # Too few public methods in the class
import json

from app.api.hvac_control_api import send_action_to_hvac
from app.services.database_service import DatabaseService


class HvacService:
    """Service class for performing actions on the HVAC system."""

    @staticmethod
    def perform_hvac_action(host, token, action_type, temperature, sensor_event_id):
        """Send the action to the HVAC system and store it."""
        try:
            # Send the action to the HVAC system and get the response
            _, response_details = send_action_to_hvac(host, token, action_type, 10)

            print(f"\nPerforming HVAC Action: {action_type}")

            # Store the HVAC action in the database
            DatabaseService.store_hvac_action(
                action_type, temperature, sensor_event_id, response_details
            )

        except (json.JSONDecodeError, TypeError, ConnectionError) as e:
            print(f"Error performing HVAC action: {e}")
