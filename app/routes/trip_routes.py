from fastapi import APIRouter, HTTPException
from app.utils.helper_functions import get_delivery_centers
from app.utils.helper_functions import fetch_ongoing_trip_counts


delivery_center_router = APIRouter()
@delivery_center_router.get("/delivery-centers")
def fetch_delivery_centers():
    """Returns all active delivery centers."""
    centers_df = get_delivery_centers()
    return centers_df.to_dict(orient="records")  # Convert DataFrame to list of dicts


ongoing_trip_router= APIRouter()

@ongoing_trip_router.get("/ongoing-trips")
def fetch_ongoing_trips():
    """
    Returns ongoing trip counts in a matrix format suitable for Power BI.
    Each row represents a `delivery_center_name`, and each column represents a `trip_date`.
    """
    try:
        trips_matrix = fetch_ongoing_trip_counts()
        if not trips_matrix:
            return {"status": "success", "message": "No ongoing trips found", "data": []}
        return {"status": "success", "data": trips_matrix}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


