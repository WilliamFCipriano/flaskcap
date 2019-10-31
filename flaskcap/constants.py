from enum import Enum, auto
from enum import unique


@unique
class SaveState(Enum):
    clean = auto()
    dirty = auto()
