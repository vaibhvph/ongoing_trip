from fastapi import FastAPI
from app.routes.trip_routes import router as trip_router

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI for Ongoing Trips is Running!"}

# Include trip routes
app.include_router(trip_router)


