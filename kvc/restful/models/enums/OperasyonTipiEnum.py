import enum


class OperasyonTipiEnum(enum.IntEnum):
    """ Operasyon tipleri için enum sınıfı """

    ANA_ISLEM = 0
    EK_ISLEM = 1

    @staticmethod
    def get_by_name(name: str):
        for e in list(OperasyonTipiEnum):
            if name == e.name:
                return e
        return None
