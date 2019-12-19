import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class KVCLabelEnum(AbstractIntEnum):
    """ KVC etiket tipleri için enum sınıfı """

    TABURCU = 0
    ENFEKTE = 1
    AMELIYAT = 2
    YOGUN_BAKIM = 3
    OLUM = 4