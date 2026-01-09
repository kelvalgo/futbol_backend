from fastapi import FastAPI
from .db.db import lifespan
from .routers import admin,auth,user_router

app = FastAPI(lifespan=lifespan)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user_router.router)



