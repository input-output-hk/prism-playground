from enum import Enum


class ActionType(str, Enum):
    ADD_KEY = "ADD_KEY"
    ADD_SERVICE = "ADD_SERVICE"
    REMOVE_KEY = "REMOVE_KEY"
    REMOVE_SERVICE = "REMOVE_SERVICE"
    UPDATE_SERVICE = "UPDATE_SERVICE"

    def __str__(self) -> str:
        return str(self.value)
