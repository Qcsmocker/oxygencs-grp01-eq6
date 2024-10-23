import requests
import json


def send_action_to_hvac(host, token, action, ticks):
    """Send control action (TurnOnAc, TurnOnHeater) to HVAC."""
    response = requests.get(f"{host}/api/hvac/{token}/{action}/{ticks}")
    details = json.loads(response.text)
    print(details)
    return response.status_code, details
