from fastapi import FastAPI
from .db.db import lifespan
from .routers import auth,user,group,invitation,skills,user_groupf,season,match,generator_team,match_player

app = FastAPI(lifespan=lifespan) 
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




