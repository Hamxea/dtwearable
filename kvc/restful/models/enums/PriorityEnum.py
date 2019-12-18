import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class PriorityEnum(AbstractIntEnum):
    """ Öncelik tipleri için enum sınıfı """

    LOW = 0
    MEDIUM = 1
    HIGH = 2