import enum


class ChoosenTypeEnum(enum.Enum):
    """Kural özellik; tahmın olan (1) ve ilk giren hemşire gözlem özellik(0)"""
    REAL = 0,
    PREDICT = 1
