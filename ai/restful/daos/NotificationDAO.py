from sqlalchemy import text

from ai.restful.daos.AbstractDAO import AbstractDAO
from db import db
from ai.restful.models.NotificationDTO import NotificationDTO


class NotificationDAO(AbstractDAO):
    """ Contains methods by which database operations are performed for the Notification object """

    def __init__(self):
        super().__init__(NotificationDTO)

    def get_by_islem_no(self, islem_no_list):
        """ method that returns Notification objects based on transaction_id values"""

        sql_text = text("select * from notification "
                        "inner join rule_violation on notification.rule_violation_id = rule_violation.id "
                        "where rule_violation.reference_table = 'action' and rule_violation.reference_id = ANY(:ids)")
        list = db.session.query(NotificationDTO).from_statement(sql_text).params(ids=islem_no_list).all()

        result = []
        for notification in list:
            result.append(notification.serialize)

        return result
