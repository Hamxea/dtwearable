from datetime import datetime
from db import db
from ai.enums.IntEnum import IntEnum
from ai.enums.PriorityEnum import PriorityEnum


class NotificationDTO(db.Model):
    """ Notification tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "notification"

    id = db.Column(db.BigInteger, primary_key=True)
    # rule_violation_id = db.Column(db.BigInteger)
    staff_id = db.Column(db.BigInteger)
    priority = db.Column(IntEnum(PriorityEnum))
    message = db.Column(db.String)
    notification_date = db.Column(db.DateTime)
    error_message = db.Column(db.String)

    def __init__(self, id: int, staff_id: int, priority: int, message: str, notification_date: datetime,
                 error_message: str):
        self.id = id
        # self.rule_violation_id = rule_violation_id
        self.staff_id = staff_id
        self.priority = priority
        self.message = message
        self.notification_date = notification_date
        self.error_message = error_message

    @property
    def serialize(self):
        """ Notification nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            # 'rule_violation_id': self.rule_violation_id,
            'staff_id': self.staff_id,
            'priority': self.priority.name,
            'message': self.message,
            'notification_date': self.notification_date.strftime('%d.%m.%Y %H:%M:%S'),
            'error_message': self.error_message,
        }
