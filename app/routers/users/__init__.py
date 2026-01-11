from fastapi import APIRouter
from .users_router import router as users_router

router = APIRouter(prefix="/user")

router.include_router(users_router)