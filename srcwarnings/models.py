from enum import IntEnum


class Severity(IntEnum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    ADVISORY = 0


class Confidence(IntEnum):
    LOW = 0,
    MEDIUM = 1
    MEDIUM_PLUS = 2
    HIGH = 3
    HIGHEST = 4