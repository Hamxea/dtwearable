import enum


class TaniTipiEnum(enum.IntEnum):
    """ Tanı tipleri için enum sınıfı """

    ANA_TANI = 0
    ESLIK_EDEN_TANI= 1

    @staticmethod
    def get_by_name(name: str):
        for e in list(TaniTipiEnum):
            if name == e.name:
                return e
        return None
