from app.api_router import api_router
from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.logger import get_logger
from app.user.model import User  # Ensure User model is imported for migrations
from app.project.model import Project  # Ensure Project model is imported for migrations
from app.task.model import Task  # Ensure Task model is imported for migrations

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management API",
    description="CRUD API for managing projects",
    version="1.0.0"
)
app.include_router(api_router, prefix="/api/v1")



logger = get_logger(__name__)


@app.get("/")
def root():
    return {"message": "Project Management API is running"}

# To run: uvicorn main:app --reload