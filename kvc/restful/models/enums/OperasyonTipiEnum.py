import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class OperasyonTipiEnum(AbstractIntEnum):
    """ Operasyon tipleri için enum sınıfı """

    ANA_ISLEM = 0
    EK_ISLEM = 1