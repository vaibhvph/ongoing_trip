from fastapi import APIRouter
from app.utils.helper_functions import get_ongoing_trip_counts

router = APIRouter()


@router.get("/ongoing-trip-matrix")
def fetch_ongoing_trip_matrix():
    """
    Returns ongoing trips in a pivot table format:
    - Rows: delivery_center_name
    - Columns: Dates
    - Values: Trip count
    """
    pivot_df = get_ongoing_trip_counts()

    # Convert DataFrame to a simple dictionary
    return pivot_df.to_dict()
