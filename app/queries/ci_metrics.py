"""
This module provides database query functions for CI metrics.
"""


def insert_ci_metrics(cursor, metrics_data):
    """
    Insert CI metrics into the ci_metrics table.

    :param cursor: Database cursor object.
    :param metrics_data: Dictionary containing metrics data with keys:
                         - timestamp
                         - build_success_rate
                         - average_build_duration
                         - tests_executed
                         - test_failure_rate
    """
    query = """
        INSERT INTO ci_metrics (timestamp, build_success_rate, average_build_duration, tests_executed, test_failure_rate)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            metrics_data["timestamp"],
            metrics_data["build_success_rate"],
            metrics_data["average_build_duration"],
            metrics_data["tests_executed"],
            metrics_data["test_failure_rate"],
        ),
    )
