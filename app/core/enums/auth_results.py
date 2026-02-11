from enum import Enum

class AuthResult(Enum):
    ALLOWED = "allowed"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"