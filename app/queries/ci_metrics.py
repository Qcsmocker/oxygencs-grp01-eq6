"""
This module provides database query functions for CI metrics.
"""

from app.queries.data_models import CIMetrics  # Updated import


def insert_ci_metrics(
    cursor,
    timestamp,
    build_success_rate,
    average_build_duration,
    tests_executed,
    test_failure_rate,
):
    """Insert CI metrics into the ci_metrics table."""
    query = """
        INSERT INTO ci_metrics (timestamp, build_success_rate, average_build_duration, tests_executed, test_failure_rate)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            timestamp,
            build_success_rate,
            average_build_duration,
            tests_executed,
            test_failure_rate,
        ),
    )
