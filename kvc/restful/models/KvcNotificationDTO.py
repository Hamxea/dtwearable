from datetime import datetime

from db import db
from kvc.restful.models.enums.IntEnum import IntEnum
from kvc.restful.models.enums.PriorityEnum import PriorityEnum


class KvcNotificationDTO(db.Model):
    """ KvcNotification tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "kvc_notification"

    id = db.Column(db.BigInteger, primary_key=True)
    rule_violation_id = db.Column(db.BigInteger)
    staff_id = db.Column(db.BigInteger)
    priority = db.Column(IntEnum(PriorityEnum), default=PriorityEnum.MEDIUM)
    message = db.Column(db.String)
    notification_date = db.Column(db.DateTime)
    error_message = db.Column(db.String)

    def __init__(self, id: int, rule_violation_id: int, staff_id: int, priority: int, message: str, notification_date:datetime, error_message: str):
        self.id = id
        self.rule_violation_id = rule_violation_id
        self.staff_id = staff_id
        self.priority = priority
        self.message = message
        self.notification_date = notification_date
        self.error_message = error_message

    @property
    def serialize(self):
        """ LabSonuc nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'rule_violation_id': self.rule_violation_id,
            'staff_id': self.staff_id,
            'priority': self.priority.name,
            'message': self.message,
            'notification_date': self.notification_date.strftime('%d.%m.%Y %H:%M:%S'),
            'error_message': self.error_message
        }