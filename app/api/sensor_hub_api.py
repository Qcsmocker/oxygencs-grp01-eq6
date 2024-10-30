"""
This module provides an interface for communicating with the sensor hub API.
"""

import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder


def negotiate(host: str, token: str) -> str:
    """Fetch the connectionId by negotiating with the server.

    :param host: The base URL of the sensor hub.
    :param token: The authentication token.
    :return: The connection ID.
    :raises requests.exceptions.RequestException: If the negotiation fails.
    """
    negotiate_url = f"{host}/SensorHub/negotiate?token={token}"
    response = requests.post(negotiate_url, timeout=10)  # Set a 10-second timeout

    if response.status_code == 200:
        data = response.json()
        return data["connectionId"]

    # Raise a more specific error
    raise requests.exceptions.RequestException(
        f"Failed to negotiate connection. Status code: {response.status_code}"
    )


def setup_sensor_hub(host: str, token: str, on_data_received) -> "HubConnectionBuilder":
    """Set up the sensor hub connection and handle incoming data.

    :param host: The base URL of the sensor hub.
    :param token: The authentication token.
    :param on_data_received: Callback function to handle incoming data.
    :return: An instance of HubConnectionBuilder configured for the sensor hub.
    """
    connection_id = negotiate(host, token)
    hub_connection = (
        HubConnectionBuilder()
        .with_url(f"{host}/SensorHub?token={token}&connectionId={connection_id}")
        .with_automatic_reconnect(
            {
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 999,
            }
        )
        .build()
    )
    hub_connection.on("ReceiveSensorData", on_data_received)
    return hub_connection
