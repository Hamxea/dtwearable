import enum

from dt.ruleengines.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class PriorityEnum(AbstractIntEnum):
    """ Enum class for priority types """

    LOW = 0
    MEDIUM = 1
    HIGH = 2