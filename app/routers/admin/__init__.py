from fastapi import APIRouter
from .users_router import router as users_router
from .skills_router import router as skills_router
from .games_table_router import router as games_table_router

router = APIRouter(prefix="/admin")

router.include_router(users_router)
router.include_router(skills_router)
router.include_router(games_table_router)