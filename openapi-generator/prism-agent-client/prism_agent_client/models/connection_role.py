from enum import Enum


class ConnectionRole(str, Enum):
    INVITEE = "Invitee"
    INVITER = "Inviter"

    def __str__(self) -> str:
        return str(self.value)
