from datetime import datetime, timedelta
import pandas as pd
from app.services.database import get_db_connection


def get_delivery_centers():
    """Fetch all ACTIVE delivery centers from the `delivery_center` table."""
    conn = get_db_connection()

    df = conn.execute("""
        SELECT delivery_center_name
        FROM delivery_center
        WHERE status = 'ACTIVE'
    """).df()

    conn.close()
    return df

def fetch_ongoing_trip_counts():
    """
    Fetch ongoing trip counts and return them in a matrix format:
    - Rows: `delivery_center_name`
    - Columns: `trip_date`
    - Values: `trip_count`
    """
    conn = get_db_connection()

    # Get yesterday's date dynamically
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Fetch ongoing trips (excluding COMPLETETRIP, CANCELLEDTRIP, etc.)
    query = """
        SELECT delivery_center_name, consignment_date
        FROM ongoing_trips
        WHERE trip_status NOT IN ('COMPLETETRIP', 'CANCELLEDTRIP', 'OFF_DUTY', 'HOLD', 'ABSENT')
        AND consignment_date BETWEEN '2025-01-01' AND '{yesterday}'
    """

    df = conn.execute(query).df()
    conn.close()

    if df.empty:
        return []

    # Convert consignment_date to datetime format
    df["consignment_date"] = pd.to_datetime(df["consignment_date"]).dt.date

    # Group by delivery center and date, then count trips
    grouped_df = df.groupby(["delivery_center_name", "consignment_date"]).size().reset_index(name="trip_count")

    # Pivot the DataFrame to make dates into columns
    pivot_df = grouped_df.pivot(index="delivery_center_name", columns="consignment_date", values="trip_count").fillna(0)

    # Reset index to return as JSON-friendly format
    pivot_df.reset_index(inplace=True)

    # Convert all column names to string (for JSON compatibility)
    pivot_df.columns = pivot_df.columns.astype(str)

    return pivot_df.to_dict(orient="records")  # Convert to list of dictionaries for JSON response

