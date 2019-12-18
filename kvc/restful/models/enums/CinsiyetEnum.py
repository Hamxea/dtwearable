import enum

from kvc.restful.models.enums.AbstractIntEnum import AbstractIntEnum


@enum.unique
class CinsiyetEnum(AbstractIntEnum):
    """ Cinsiyet tipleri için enum sınıfı """

    ERKEK = 0
    KADIN = 1
