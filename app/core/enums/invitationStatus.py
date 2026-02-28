from enum import Enum


class InvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
