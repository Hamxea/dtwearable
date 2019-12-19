from sqlalchemy import text

from ai.restful.daos.AbstractDAO import AbstractDAO
from db import db
from ai.restful.models.NotificationDTO import NotificationDTO


class NotificationDAO(AbstractDAO):
    """ Notification nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(NotificationDTO)

    def get_by_islem_no(self, islem_no_list):
        """ islem_no değerlerine göre Notification nesnelerini dönen metod """

        sql_text = text("select * from notification "
                        "inner join rule_violation on notification.rule_violation_id = rule_violation.id "
                        "where rule_violation.reference_table = 'islem' and rule_violation.reference_id = ANY(:ids)")
        list = db.session.query(NotificationDTO).from_statement(sql_text).params(ids=islem_no_list).all()

        result = []
        for notification in list:
            result.append(notification.serialize)

        return result
