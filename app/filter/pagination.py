
from fastapi import Query
from pydantic import BaseModel

class Pagination(BaseModel):
    skip: int = Query(0, ge=0, description="Records to skip")
    limit: int = Query(10, ge=1, le=10, description="Records limit")