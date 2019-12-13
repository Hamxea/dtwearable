from flask_restful import Resource

from kvc.restful.daos.KvcNotificationDAO import KvcNotificationDAO


class KvcNotificationResource(Resource):
    """
    KvcNotificationResource nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    dao = KvcNotificationDAO()

    def get(self, kvc_notification_id: int):
        """ kvc_notification_id parametresine karsılık KvcNotificationDTO bilgisi donen metod """

        kvc_notification_dto = self.dao.find_by_id(kvc_notification_id)
        if not kvc_notification_dto:
            return {'message': 'Object Not Found'}, 404
        return kvc_notification_dto.serialize, 200

    def delete(self, kvc_notification_id: int):
        """ kvc_notification_id parametresine göre KvcNotificationDTO nesnesini donen metod """

        kvc_notification_dto = self.dao.find_by_id(kvc_notification_id)
        if not kvc_notification_dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(kvc_notification_dto)
        return {'message': 'Object deleted.'}, 200
