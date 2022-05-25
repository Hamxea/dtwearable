from flask_restful import Resource

from ai.restful.daos.NotificationDAO import NotificationDAO


class NotificationResource(Resource):
    """
    Resource class that hosts methods that take int type id parameter for NotificationResource object
     Methods are created to respond to Restful request types
    """

    dao = NotificationDAO()

    def get(self, notification_id: int):
        """ Method that returns NotificationDTO information corresponding to notification_id parameter """

        notification_dto = self.dao.find_by_id(notification_id)
        if not notification_dto:
            return {'message': 'Object Not Found'}, 404
        return notification_dto.serialize, 200

    def delete(self, notification_id: int):
        """ Method that deletes NotificationDTO object based on notification_id parameter """

        notification_dto = self.dao.find_by_id(notification_id)
        if not notification_dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(notification_dto)
        return {'message': 'Object deleted.'}, 200
