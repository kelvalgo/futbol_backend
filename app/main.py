from fastapi import FastAPI,Request
from .db.db import lifespan
from .routers import auth,user,group,invitation,skills,user_groupf,season,match,generator_team,match_player

from dotenv import load_dotenv
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

app = FastAPI(lifespan=lifespan) 

# 🔹 cargar variables de entorno
load_dotenv()

# 🔹 registrar limiter
app.state.limiter = limiter

# 🔹 middleware de slowapi
app.add_middleware(SlowAPIMiddleware)

# 🔹 handler de error
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )






app.include_router(auth.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(invitation.router)
app.include_router(skills.router)
app.include_router(user_groupf.router)
app.include_router(season.router)
app.include_router(match.router)
app.include_router(generator_team.router)
app.include_router(match_player.router)




