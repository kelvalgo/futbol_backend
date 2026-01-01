from fastapi import FastAPI
from app.db.db import lifespan
from .routers import player_router,auth

app = FastAPI(lifespan=lifespan)
app.include_router(player_router.router)
app.include_router(auth.router)



