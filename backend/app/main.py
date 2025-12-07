from app.api_router import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.logger import get_logger
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management API",
    description="CRUD API for managing projects",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(api_router, prefix="/api/v1")



logger = get_logger(__name__)


@app.get("/")
def root():
    return {"message": "Project Management API is running"}

# To run: uvicorn main:app --reload