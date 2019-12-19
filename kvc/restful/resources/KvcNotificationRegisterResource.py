from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.restful.daos.KvcNotificationDAO import KvcNotificationDAO
from kvc.restful.models.KvcNotificationDTO import KvcNotificationDTO
from kvc.restful.models.enums.PriorityEnum import PriorityEnum


class KvcNotificationRegisterResource(Resource):
    """
    KvcNotificationDTO nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False)
    post_parser.add_argument('rule_violation_id', type=int, required=True)
    post_parser.add_argument('staff_id', type=int, required=True)
    post_parser.add_argument('priority', type=str, required=True)
    post_parser.add_argument('message', type=str, required=True)
    post_parser.add_argument('notification_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(), required=True)
    post_parser.add_argument('error_message', type=str, required=False)

    dao = KvcNotificationDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore KvcNotificationDTO nesnesini olusturan ve veritabanına yazan metod """

        data = self.post_parser.parse_args()

        try:
            kvc_notification_dto = KvcNotificationDTO(None, data['rule_violation_id'], data['staff_id'],
                                                      PriorityEnum.get_by_name(data['priority']),
                                                      data['message'], data['notification_date'], data['error_message'])
            self.dao.save_to_db(kvc_notification_dto)
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500

        return kvc_notification_dto.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore KvcNotificationDTO nesnesini olusturan veya guncelleyen metod """

        data = self.post_parser.parse_args()

        kvc_notification_dto = self.dao.find_by_id(data['id'])

        if kvc_notification_dto:
            kvc_notification_dto.rule_violation_id = data['rule_violation_id']
            kvc_notification_dto.staff_id = data['staff_id']
            kvc_notification_dto.priority = PriorityEnum.get_by_name(data['priority'])
            kvc_notification_dto.message = data['message']
            kvc_notification_dto.notification_date = data['notification_date']
            kvc_notification_dto.error_message = data['error_message']
        else:
            kvc_notification_dto = KvcNotificationDTO(**data)

        self.dao.save_to_db(kvc_notification_dto)

        return kvc_notification_dto.serialize
