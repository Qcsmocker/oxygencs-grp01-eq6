"""
This module provides database query functions related to HVAC actions.
"""

import json
import requests


def send_action_to_hvac(host, token, action, ticks):
    """Send control action (TurnOnAc, TurnOnHeater) to HVAC."""
    try:
        response = requests.get(f"{host}/api/hvac/{token}/{action}/{ticks}", timeout=10)

        # Check if the response is JSON
        if response.headers.get("Content-Type") == "application/json":
            details = response.json()
        else:
            # Handle non-JSON responses
            details = {
                "error": "Unexpected response format",
                "content": response.text[:200],
            }  # Limit content size for display

        return response.status_code, details

    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return 500, {"error": "Response was not in JSON format"}
    except requests.RequestException as e:
        # Handle request errors
        return 500, {"error": str(e)}
