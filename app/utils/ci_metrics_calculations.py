from psycopg2 import DatabaseError
from app.db.connection import get_db_connection, close_db_connection
from app.utils.datetime_utils import get_current_timestamp


class CIMetricsCalculator:
    """Class for calculating CI-related metrics from the database."""

    @staticmethod
    def calculate_build_success_rate():
        """Calculate the percentage of successful builds over the last minute."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            current_time = get_current_timestamp()

            # Sample calculation for successful builds
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ci_metrics
                WHERE build_success_rate >= 0 AND timestamp >= (CAST(%s AS TIMESTAMP) - INTERVAL '1 minute')
                """,
                (current_time,),
            )
            successful_builds = cursor.fetchone()[0]

            # Sample total builds calculation
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ci_metrics
                WHERE timestamp >= (CAST(%s AS TIMESTAMP) - INTERVAL '1 minute')
                """,
                (current_time,),
            )
            total_builds = cursor.fetchone()[0]

            cursor.close()
            close_db_connection(conn)

            if total_builds == 0:
                return 0.0  # Avoid division by zero if no builds exist

            return (
                successful_builds / total_builds
            ) * 100.0  # Success rate as percentage

        except DatabaseError as db_err:
            print(f"Database error while calculating build success rate: {db_err}")
            return 0.0
        except Exception as err:
            print(f"Error calculating build success rate: {err}")
            return 0.0

    @staticmethod
    def calculate_average_build_duration():
        """Calculate the average duration of builds over the last minute."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            current_time = get_current_timestamp()

            # Average build duration in the last minute
            cursor.execute(
                """
                SELECT AVG(average_build_duration)
                FROM ci_metrics
                WHERE timestamp >= (CAST(%s AS TIMESTAMP) - INTERVAL '1 minute')
                """,
                (current_time,),
            )
            average_duration = cursor.fetchone()[0] or 0.0  # Default to 0 if no data

            cursor.close()
            close_db_connection(conn)

            return average_duration

        except DatabaseError as db_err:
            print(f"Database error while calculating average build duration: {db_err}")
            return 0.0
        except Exception as err:
            print(f"Error calculating average build duration: {err}")
            return 0.0

    @staticmethod
    def calculate_tests_executed():
        """Calculate the number of tests executed over the last minute."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            current_time = get_current_timestamp()

            # Count tests executed in the last minute
            cursor.execute(
                """
                SELECT SUM(tests_executed)
                FROM ci_metrics
                WHERE timestamp >= (CAST(%s AS TIMESTAMP) - INTERVAL '1 minute')
                """,
                (current_time,),
            )
            tests_executed = cursor.fetchone()[0] or 0  # Default to 0 if no data

            cursor.close()
            close_db_connection(conn)

            return tests_executed

        except DatabaseError as db_err:
            print(f"Database error while calculating tests executed: {db_err}")
            return 0
        except Exception as err:
            print(f"Error calculating tests executed: {err}")
            return 0

    @staticmethod
    def calculate_test_failure_rate():
        """Calculate the percentage of failed tests over the last minute."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            current_time = get_current_timestamp()

            # Count failed tests in the last minute
            cursor.execute(
                """
                SELECT AVG(test_failure_rate)
                FROM ci_metrics
                WHERE timestamp >= (CAST(%s AS TIMESTAMP) - INTERVAL '1 minute')
                """,
                (current_time,),
            )
            failure_rate = cursor.fetchone()[0] or 0.0  # Default to 0 if no data

            cursor.close()
            close_db_connection(conn)

            return failure_rate

        except DatabaseError as db_err:
            print(f"Database error while calculating test failure rate: {db_err}")
            return 0.0
        except Exception as err:
            print(f"Error calculating test failure rate: {err}")
            return 0.0

    @staticmethod
    def calculate_ci_metrics():
        """Unified function to calculate and return all CI metrics."""
        build_success_rate = CIMetricsCalculator.calculate_build_success_rate()
        average_build_duration = CIMetricsCalculator.calculate_average_build_duration()
        tests_executed = CIMetricsCalculator.calculate_tests_executed()
        test_failure_rate = CIMetricsCalculator.calculate_test_failure_rate()

        # Get the current timestamp for CI metrics
        current_time = get_current_timestamp()

        return {
            "timestamp": current_time,
            "build_success_rate": build_success_rate,
            "average_build_duration": average_build_duration,
            "tests_executed": tests_executed,
            "test_failure_rate": test_failure_rate,
        }
