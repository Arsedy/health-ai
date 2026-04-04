from fastapi import APIRouter
from app.api.endpoints import analyze

router = APIRouter()

# Include the analyze endpoint
router.include_router(analyze.router)