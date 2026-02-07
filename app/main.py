from fastapi import FastAPI
from .db.db import lifespan
from .routers.admin import router as admin_router
from .routers import auth,user#,user_router
from .routers.users import router as users_router

app = FastAPI(lifespan=lifespan) 
#app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
#app.include_router(admin_router)
#app.include_router(users_router)




