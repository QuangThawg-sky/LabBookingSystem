
from fastapi import FastAPI
from datetime import datetime, timezone

from app.routers.auth import router as auth_router
from app.routers.rooms import router as rooms_router
from app.routers.equipment import router as equipment_router


app = FastAPI(
    title="Lab Booking System API",
    description="REST API quản lý đặt lịch phòng thực hành và thiết bị",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(equipment_router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Lab Booking System API",
        "project": "Lab Booking System",
        "version": "1.0.0"
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "Lab Booking System API",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
