from ..db.connection import close_db_connection, get_db_connection
from ..queries.sensor_data import insert_sensor_data
from ..queries.hvac_action import insert_hvac_action
from ..queries.ci_metrics import insert_ci_metrics


class DatabaseService:
    """Service class for database operations."""

    @staticmethod
    def store_sensor_data(sensor_data):
        """Store sensor data in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Ensure correct data fields for sensor_data
            insert_sensor_data(
                cursor, sensor_data["timestamp"], sensor_data["temperature"]
            )

            cursor.execute("SELECT LASTVAL();")
            sensor_event_id = cursor.fetchone()[0]
            conn.commit()

            return sensor_event_id

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inserting sensor data: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)

    @staticmethod
    def store_hvac_action(hvac_action):
        """Store HVAC action in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Use the HvacAction instance directly
            insert_hvac_action(cursor, hvac_action)

            cursor.execute("SELECT LASTVAL();")
            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inserting HVAC action: {e}")
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)

    @staticmethod
    def store_ci_metrics(ci_metrics):
        """Store CI metrics in the database."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Ensure correct data fields for ci_metrics
            insert_ci_metrics(
                cursor,
                ci_metrics["timestamp"],
                ci_metrics["build_success_rate"],
                ci_metrics["average_build_duration"],
                ci_metrics["tests_executed"],
                ci_metrics["test_failure_rate"],
            )

            cursor.execute("SELECT LASTVAL();")
            conn.commit()

            print(f"CI Metrics inserted successfully.")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inserting CI Metrics data: {e}")
        finally:
            if conn:
                cursor.close()
                close_db_connection(conn)
