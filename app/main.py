from fastapi import FastAPI
from .db.db import lifespan
from .routers import admin,auth

app = FastAPI(lifespan=lifespan)
app.include_router(admin.router)
app.include_router(auth.router)



