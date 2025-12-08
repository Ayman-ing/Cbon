from fastapi import APIRouter
from app.project.routes import router as project_router
from app.user.routes import router as user_router
from app.user.auth_routes import router as auth_router
from app.task.routes import router as task_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(project_router)
api_router.include_router(user_router)
api_router.include_router(task_router)
