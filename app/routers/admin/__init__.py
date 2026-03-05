from fastapi import APIRouter
from .users_router import router as users_router
from .games_table_router import router as games_table_router
#from ..season import router as season_router
from .match_router import router as match_router
from .match_player_router import router as match_player_router
from .generate_teams import router as generate_teams

router = APIRouter(prefix="/admin")

router.include_router(users_router)
#router.include_router(season_router)
router.include_router(match_router)
router.include_router(match_player_router)
router.include_router(games_table_router)
router.include_router(generate_teams)
