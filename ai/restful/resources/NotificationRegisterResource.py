import json
from datetime import datetime

from flask_restful import reqparse, Resource
from flask_socketio import emit, send

from ai.restful.daos.NotificationDAO import NotificationDAO
from ai.restful.models.NotificationDTO import NotificationDTO
from ai.enums.PriorityEnum import PriorityEnum
from ai.restful.services.RuleViolationService import RuleViolationService


class NotificationRegisterResource(Resource):
    """
    Resource class that hosts methods that do not take parameters for the NotificationDTO object
     Methods are created to respond to Restful request types
    """

    """ It is created to define Restful requests, error returns in case of incompatibility. """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False)
    # post_parser.add_argument('rule_violation_id', type=int, required=True)
    post_parser.add_argument('staff_id', type=int, required=True)
    post_parser.add_argument('priority', type=str, required=True)
    post_parser.add_argument('message', type=str, required=True)
    post_parser.add_argument('notification_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                             required=True)
    post_parser.add_argument('error_message', type=str, required=False)

    dao = NotificationDAO()
    rule_violation_service = RuleViolationService()

    def post(self):
        """ The method that creates the NotificationDTO object according to the data in the body of the Restful request and writes it to the database """

        data = self.post_parser.parse_args()

        try:
            notification_dto = NotificationDTO(None, data['staff_id'], PriorityEnum.get_by_name(data['priority']),
                                               data['message'], data['notification_date'], data['error_message'])
            self.dao.save_to_db(notification_dto)

            emit('message', notification_dto.serialize, broadcast=True, namespace='/')
            # emit('message', json.dumps(notification_dto.serialize), broadcast=True,namespace='/ai/notification')
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500

        return notification_dto.serialize, 201

    def put(self):
        """ The method that creates or updates the NotificationDTO object according to the data contained in the body of the Restful request """

        data = self.post_parser.parse_args()

        notification_dto = self.dao.find_by_id(data['id'])

        if notification_dto:
            # notification_dto.rule_violation_id = data['rule_violation_id']
            notification_dto.staff_id = data['staff_id']
            notification_dto.priority = PriorityEnum.get_by_name(data['priority'])
            notification_dto.message = data['message']
            notification_dto.notification_date = data['notification_date']
            notification_dto.error_message = data['error_message']
        else:
            notification_dto = NotificationDTO(**data)

        emit('message', notification_dto.serialize, broadcast=True, namespace='/')
        self.dao.save_to_db(notification_dto)

        return notification_dto.serialize
