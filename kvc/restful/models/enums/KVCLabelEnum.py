import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class KVCLabelEnum(AbstractIntEnum):
    """ KVC etiket tipleri için enum sınıfı """

    BELIRSIZ = 0
    TABURCU = 1
    ENFEKTE = 2
    AMELIYAT = 3
    YOGUN_BAKIM = 4
    OLUM = 5