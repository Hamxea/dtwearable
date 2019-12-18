import enum

@enum.unique
class AbstractIntEnum(enum.IntEnum):
    """ IntEnum sınıfları için ihtiyaç duyulan abstract metodların tanımlandığı üst sınıf """

    @classmethod
    def get_by_name(cls, name: str):
        """ Enum ismine göre Enum örneğini dönen metod """

        for e in list(cls):
            if name == e.name:
                return e
        raise NotImplementedError("Enum not found in {}".format(cls.__name__))