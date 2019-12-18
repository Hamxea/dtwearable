import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class TaniTipiEnum(AbstractIntEnum):
    """ Tanı tipleri için enum sınıfı """

    ANA_TANI = 0
    ESLIK_EDEN_TANI= 1