import enum


class CinsiyetEnum(enum.IntEnum):
    """ Cinsiyet tipleri için enum sınıfı """

    ERKEK = 0
    KADIN = 1

    @staticmethod
    def get_by_name(name: str):
        for e in list(CinsiyetEnum):
            if name == e.name:
                return e
        return None