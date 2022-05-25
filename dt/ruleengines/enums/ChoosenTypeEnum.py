import enum


class ChoosenTypeEnum(enum.Enum):
    """ Rule Engine; Prediction (1) Real Measured Values(0)"""
    REAL = 0,
    PREDICT = 1
