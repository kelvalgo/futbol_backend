from typing import Optional
from pydantic import Field
from .pagination import Pagination
from app.core.enums.status_enum import Status

class UserFilter(Pagination):
    group_id: int
    role: Optional[str] = None
    is_active: Status = Field(default=Status.active)