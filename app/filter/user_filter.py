from typing import Optional
from .pagination import Pagination

class UserFilter(Pagination):
    group_id: int
    role: Optional[str] = None
    active: Optional[bool] = None