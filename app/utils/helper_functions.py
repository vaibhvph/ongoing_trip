import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.services.database import get_db_connection

# loading environment variables
load_dotenv()


def get_ongoing_trip_counts():
    """
    Creates a DataFrame where:
    - Rows: `delivery_center_name`
    - Columns: Dates from `calendar_table` (filtered from 2025-01-01 to yesterday)
    - Values: Count of ongoing trips per delivery center per date.
    """

    trips_df = get_ongoing_trips()
    if trips_df.empty:
        raise ValueError("No ongoing trips found.")

    # Fetch only 2025 calendar dates (2025-01-01 to yesterday)
    calendar_df = get_calendar_dates()

    # Convert date columns to datetime for consistency
    trips_df['trip_date'] = pd.to_datetime(trips_df['consignment_date'])
    calendar_df['date'] = pd.to_datetime(calendar_df['date'])

    # Create pivot table: count ongoing trips per day per delivery center
    pivot_df = trips_df.pivot_table(
        index="delivery_center_name",
        columns="trip_date",
        values="trip_id",
        aggfunc="count",
        fill_value=0
    )

    # Ensure all calendar dates are included in columns
    pivot_df = pivot_df.reindex(columns=calendar_df['date'], fill_value=0)

    # Reset index to match Power BI format
    pivot_df = pivot_df.reset_index()

    # Convert date columns to string format (Power BI prefers this)
    pivot_df.columns = ['delivery_center_name'] + [str(col.date()) for col in pivot_df.columns[1:]]

    return pivot_df


def get_ongoing_trips():
    conn = get_db_connection()
    df = conn.execute("""
        select trip_id, consignment_date, delivery_center_name, trip_status
        from ongoing_trips
        where consignment_date >= '2025-01-01'
    """).df()
    conn.close()

    # Filter only required trip statuses using Pandas
    df = df[~df['trip_status'].isin(['COMPLETETRIP', 'CANCELLEDTRIP', 'OFF_DUTY', 'HOLD', 'ABSENT'])]

    return df


def get_calendar_dates():
    conn = get_db_connection()
    df = conn.execute("select date from calendar where date >= '2025-01-01'").df()
    conn.close()

    # Convert to datetime and filter dynamically
    df['date'] = pd.to_datetime(df['date'])

    # Get yesterday's date dynamically
    yesterday = datetime.today() - timedelta(days=1)

    df = df[df['date'] <= yesterday]
    return df
