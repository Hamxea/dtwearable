import enum


class PriorityEnum(enum.IntEnum):
    """ Öncelik tipleri için enum sınıfı """

    LOW = 0
    MEDIUM = 1
    HIGH = 2

    @staticmethod
    def get_by_name(name: str):
        for e in list(PriorityEnum):
            if name == e.name:
                return e
        return None