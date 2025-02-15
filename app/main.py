from fastapi import FastAPI
from app.routes.trip_routes import  delivery_center_router, ongoing_trip_router

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI for Ongoing Trips is Running!"}

# Include trip routes
app.include_router(delivery_center_router)
app.include_router(ongoing_trip_router)