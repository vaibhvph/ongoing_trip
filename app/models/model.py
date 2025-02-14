from pydantic import BaseModel
from typing import Optional
from datetime import date

class OngoingTrip(BaseModel):
    trip_id: int
    trip_status: str
    delivery_center_id: int
    delivery_center_name: str
    client_id: int
    client_name: str
    consignment_date: date
    region: Optional[str] = None  # Optional field
