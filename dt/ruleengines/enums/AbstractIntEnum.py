import enum

@enum.unique
class AbstractIntEnum(enum.IntEnum):
    """ superclass that defines the abstract methods needed for IntEnum classes """

    @classmethod
    def get_by_name(cls, name: str):
        """ Method returning Enum instance by enum name """

        for e in list(cls):
            if name == e.name:
                return e
        raise NotImplementedError("Enum not found in {}".format(cls.__name__))