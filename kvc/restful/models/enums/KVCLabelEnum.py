import enum


class KVCLabelEnum(enum.IntEnum):
    """ KVC etiket tipleri için enum sınıfı """

    TABURCU = 0
    ENFEKTE = 1
    AMELIYAT = 2
    YOGUN_BAKIM = 3
    OLUM = 4

    @staticmethod
    def get_by_name(name: str):
        for e in list(KVCLabelEnum):
            if name == e.name:
                return e
        return None