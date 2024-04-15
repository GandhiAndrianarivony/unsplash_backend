from enum import Enum


class Enumeration(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __str__(self):
        return f"{self.value}"
