from sqlalchemy import text

from ai.restful.daos.AbstractDAO import AbstractDAO
from db import db
from kvc.restful.models.KvcNotificationDTO import KvcNotificationDTO


class KvcNotificationDAO(AbstractDAO):
    """ KvcNotification nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(KvcNotificationDTO)

    def get_by_islem_no(self, islem_no_list):
        """ islem_no değerlerine göre KvcNotification nesnelerini dönen metod """

        sql_text = text("select * from kvc_notification "
                        "inner join rule_violation on kvc_notification.rule_violation_id = rule_violation.id "
                        "inner join islem on rule_violation.islem_id = islem.id "
                        "where islem.islem_no = ANY(:ids)")
        list = db.session.query(KvcNotificationDTO).from_statement(sql_text).params(ids=islem_no_list).all()

        result = []
        for kvc_notification in list:
            result.append(kvc_notification.serialize)

        return result
