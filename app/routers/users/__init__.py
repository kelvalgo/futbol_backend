'''
from fastapi import APIRouter
from .get_router import router as get_router
from .new_pass_router import router as new_pass_router

router = APIRouter(prefix="/user")

router.include_router(get_router)
router.include_router(new_pass_router)
'''