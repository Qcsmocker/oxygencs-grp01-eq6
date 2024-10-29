"""
This module provides a service for calculating and updating CI metrics
in the database.
"""

# pylint: disable=E1121, R0903
from psycopg2 import DatabaseError

from app.db.connection import close_db_connection, get_db_connection
from app.utils.ci_metrics_calculations import CIMetricsCalculator
from app.utils.datetime_utils import get_current_timestamp


class CIMetricsService:
    """Service class for interacting with CI metrics in the database."""

    @staticmethod
    def update_ci_metrics():
        """Calculate and insert CI-related metrics into the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            current_time = get_current_timestamp()

            # Calculate metrics using the calculator
            build_success_rate = CIMetricsCalculator.calculate_build_success_rate(
                cursor, current_time
            )
            average_build_duration = (
                CIMetricsCalculator.calculate_average_build_duration(
                    cursor, current_time
                )
            )
            tests_executed = CIMetricsCalculator.calculate_tests_executed(
                cursor, current_time
            )
            test_failure_rate = CIMetricsCalculator.calculate_test_failure_rate(
                cursor, current_time
            )

            # Insert the updated metrics back to the database
            cursor.execute(
                """
                INSERT INTO ci_metrics (
                    timestamp,
                    build_success_rate,
                    average_build_duration,
                    tests_executed,
                    test_failure_rate
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    current_time,
                    build_success_rate,
                    average_build_duration,
                    tests_executed,
                    test_failure_rate,
                ),
            )

            conn.commit()
            print("CI Metrics updated successfully.")

        except DatabaseError as db_err:
            print(f"Database error while updating CI metrics: {db_err}")
        except (TypeError, ValueError) as err:
            print(f"Error updating CI metrics: {err}")
        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
