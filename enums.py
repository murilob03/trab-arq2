from enum import Enum


class MESITag(Enum):
    M = "M"
    E = "E"
    S = "S"
    I = "I"


class BloodType(Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

    def __str__(self) -> str:
        if len(self.value) < 3:
            return self.value + ' '
        return self.value


class SnoopMessage(Enum):
    READ = "read"
    READ_WITH_INTENT_TO_MODIFY = "rwitm"
    INVALIDATE = "invalidate"
