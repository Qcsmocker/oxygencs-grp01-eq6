"""
This module provides database query functions related to HVAC actions.
"""

import requests
import json


def send_action_to_hvac(host, token, action, ticks):
    """Send control action (TurnOnAc, TurnOnHeater) to HVAC."""
    response = requests.get(f"{host}/api/hvac/{token}/{action}/{ticks}")
    details = json.loads(response.text)
    return response.status_code, details
