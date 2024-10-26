import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from app.main import App
from unittest.mock import patch


class TestHVACLogic(unittest.TestCase):
    @patch("time.sleep", return_value=None)  # Mock time.sleep to prevent actual waiting
    def test_heater_on_for_below_t_min(self, mock_sleep):
        """Test for turning on the Heater when temperature is below T_MIN."""

        app = App()
        app.heater_on = False
        app.ac_on = True  # Assume AC is on initially
        app.ticks = 10
        temperature = app.t_min - 1  # Below T_MIN

        app.take_action(temperature, sensor_event_id=1)

        # Verify that the Heater was turned on and AC was turned off
        self.assertTrue(app.heater_on, "Heater should be on.")
        self.assertFalse(app.ac_on, "AC should be off.")

        # Simulate the passage of time for ticks
        for _ in range(app.ticks):
            app.take_action(
                temperature, sensor_event_id=1
            )  # Call take_action for ticks duration
        self.assertTrue(app.heater_on, "Heater should remain on after ticks.")
        self.assertFalse(app.ac_on, "AC should remain off after ticks.")

    @patch("time.sleep", return_value=None)
    def test_ac_on_for_above_t_max(self, mock_sleep):
        """Test for turning on the AC when temperature is above T_MAX."""

        app = App()
        app.heater_on = True  # Assume Heater is on initially
        app.ac_on = False
        app.ticks = 10
        temperature = app.t_max + 1  # Above T_MAX

        app.take_action(temperature, sensor_event_id=2)

        # Verify that AC was turned on and Heater was turned off
        self.assertTrue(app.ac_on, "AC should be on.")
        self.assertFalse(app.heater_on, "Heater should be off.")

        # Simulate the passage of time for ticks
        for _ in range(app.ticks):
            app.take_action(
                temperature, sensor_event_id=2
            )  # Call take_action for ticks duration
        self.assertTrue(app.ac_on, "AC should remain on after ticks.")
        self.assertFalse(app.heater_on, "Heater should remain off after ticks.")

    @patch("time.sleep", return_value=None)
    def test_turn_off_ac_and_heater_within_range(self, mock_sleep):
        """Test for turning off AC and Heater when temperature is within range."""

        app = App()
        app.heater_on = True  # Heater is on
        app.ac_on = True  # AC is on
        app.ticks = 10
        temperature = (app.t_min + app.t_max) / 2  # Within range

        app.take_action(temperature, sensor_event_id=3)

        # Verify both AC and Heater are off
        self.assertFalse(app.ac_on, "AC should be off.")
        self.assertFalse(app.heater_on, "Heater should be off.")

        # Simulate the passage of time for ticks
        for _ in range(app.ticks):
            app.take_action(
                temperature, sensor_event_id=3
            )  # Call take_action for ticks duration


if __name__ == "__main__":
    unittest.main()
