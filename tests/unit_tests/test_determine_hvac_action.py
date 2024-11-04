"""
Unit tests for the determine_hvac_action method in the App class.
This module tests various temperature scenarios to ensure
the correct HVAC actions are performed.
"""

# pylint: disable=E0401
import unittest
from unittest.mock import patch
from dotenv import load_dotenv
from app.main import App  # Import the main App class

# Load environment variables from .env file
load_dotenv()


class TestDetermineHvacAction(unittest.TestCase):
    """Tests for the determine_hvac_action method in the App class."""

    def setUp(self):
        """Set up the App instance with default configuration for each test."""
        self.app = App()
        self.app.config["t_min"] = 18.0
        self.app.config["t_max"] = 24.0
        self.app.ac_on = False
        self.app.heater_on = False

    @patch.object(App, "perform_hvac_action")
    def test_turn_on_heater_when_temp_below_t_min(self, mock_perform_hvac_action):
        """Test that the heater is turned on when temperature is below t_min."""
        self.app.determine_hvac_action(15.0, sensor_event_id=1)
        mock_perform_hvac_action.assert_any_call("TurnOnHeater", 15.0, 1)
        self.assertTrue(
            self.app.heater_on, "Heater should be on when temperature is below t_min"
        )

    @patch.object(App, "perform_hvac_action")
    def test_turn_on_ac_when_temp_above_t_max(self, mock_perform_hvac_action):
        """Test that the AC is turned on when temperature is above t_max."""
        self.app.determine_hvac_action(26.0, sensor_event_id=2)
        mock_perform_hvac_action.assert_any_call("TurnOnAc", 26.0, 2)
        self.assertTrue(
            self.app.ac_on, "AC should be on when temperature is above t_max"
        )

    @patch.object(App, "perform_hvac_action")
    def test_turn_off_heater_when_temp_within_range(self, mock_perform_hvac_action):
        """Test that the heater is turned off when temperature is within the acceptable range."""
        self.app.heater_on = True
        self.app.determine_hvac_action(20.0, sensor_event_id=3)
        mock_perform_hvac_action.assert_any_call("TurnOffHeater", 20.0, 3)
        self.assertFalse(
            self.app.heater_on, "Heater should be off when temperature is within range"
        )

    @patch.object(App, "perform_hvac_action")
    def test_turn_off_ac_when_temp_within_range(self, mock_perform_hvac_action):
        """Test that the AC is turned off when temperature is within the acceptable range."""
        self.app.ac_on = True
        self.app.determine_hvac_action(22.0, sensor_event_id=4)
        mock_perform_hvac_action.assert_any_call("TurnOffAc", 22.0, 4)
        self.assertFalse(
            self.app.ac_on, "AC should be off when temperature is within range"
        )


if __name__ == "__main__":
    unittest.main()
