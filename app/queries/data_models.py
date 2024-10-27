"""
This module contains data models used for database interactions.

These data classes represent the structure of the data
for HVAC actions, sensor data, and CI metrics.
"""

from dataclasses import dataclass


@dataclass
class HvacAction:
    """Data class for HVAC action."""
    action_timestamp: str
    action_type: str
    temperature: float
    sensor_event_id: int
    response_details: str


@dataclass
class SensorData:
    """Data class for sensor data."""
    timestamp: str
    temperature: float


@dataclass
class CIMetrics:
    """Data class for CI metrics."""
    timestamp: str
    build_success_rate: float
    average_build_duration: float
    tests_executed: int
    test_failure_rate: float
