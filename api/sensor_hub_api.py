import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder


def negotiate(host, token):
    """Fetch the connectionId by negotiating with the server."""
    negotiate_url = f"{host}/SensorHub/negotiate?token={token}"
    response = requests.post(negotiate_url)

    if response.status_code == 200:
        data = response.json()
        return data["connectionId"]
    else:
        raise Exception(
            f"Failed to negotiate connection. Status code: {response.status_code}"
        )


def setup_sensor_hub(host, token, on_data_received):
    """Set up the sensor hub connection and handle incoming data."""
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
