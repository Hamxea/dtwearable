from flask_restful import Resource

from ai.restful.daos.NotificationDAO import NotificationDAO


class NotificationResource(Resource):
    """
    NotificationResource nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    dao = NotificationDAO()

    def get(self, notification_id: int):
        """ notification_id parametresine karsılık NotificationDTO bilgisi donen metod """

        notification_dto = self.dao.find_by_id(notification_id)
        if not notification_dto:
            return {'message': 'Object Not Found'}, 404
        return notification_dto.serialize, 200

    def delete(self, notification_id: int):
        """ notification_id parametresine göre NotificationDTO nesnesini silen metod """

        notification_dto = self.dao.find_by_id(notification_id)
        if not notification_dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(notification_dto)
        return {'message': 'Object deleted.'}, 200
