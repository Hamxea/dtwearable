from datetime import datetime

from ai.enums.IntEnum import IntEnum
from ai.enums.PriorityEnum import PriorityEnum
from db import db


class RuleViolationDTO(db.Model):
    """ Rule_Violation tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "rule_violation"

    id = db.Column(db.BigInteger, primary_key=True)
    reference_table = db.Column(db.String)
    reference_id = db.Column(db.BigInteger)
    prediction_id = db.Column(db.BigInteger)
    rule = db.Column(db.Enum(PriorityEnum))
    value_source = db.Column(db.String)
    value = db.Column(db.Float)
    violation_date = db.Column(db.DateTime)
    notification_id = db.Column(db.BigInteger)
    priority = db.Column(IntEnum(PriorityEnum))

    def __init__(self, id: int, reference_table: str, reference_id: int, prediction_id: int, rule: str,
                 value_source: str, value: float, violation_date: datetime, notification_id: int, priority: int):
        self.id = id
        self.reference_table = reference_table
        self.reference_id = reference_id
        self.prediction_id = prediction_id
        self.rule = rule
        self.value_source = value_source
        self.value = value
        self.violation_date = violation_date
        self.notification_id = notification_id
        self.priority = priority

    @property
    def serialize(self):
        """ Rule_Violation nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'reference_table': self.reference_table,
            'reference_id': self.reference_id,
            'prediction_id': self.prediction_id,
            'rule': self.rule,
            'value_source': self.value_source,
            'value': self.value,
            'violation_date': self.violation_date.strftime('%d.%m.%Y %H:%M:%S'),
            'notification_id': self.notification_id,
            'priority': self.priority
        }
