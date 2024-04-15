from enum import Enum

import strawberry

from infinix.enum import Enumeration


@strawberry.enum
class GenderType(Enumeration):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
