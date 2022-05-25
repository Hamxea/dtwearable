from datetime import datetime

from flask_restful import reqparse, Resource

from ai.enums.PriorityEnum import PriorityEnum
from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO


class RuleViolationRegisterResource(Resource):
    """
    Resource class that hosts methods that do not take parameters for the RuleViolationDTO object
     Methods are created to respond to Restful request types
    """

    """ Created to define Restful requests, error returns in case of incompatibility. """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False)
    post_parser.add_argument('reference_table', type=str, required=True)
    post_parser.add_argument('reference_id', type=int, required=True)
    post_parser.add_argument('prediction_id', type=int, required=True)
    post_parser.add_argument('rule', type=str, required=True)
    post_parser.add_argument('value_source', type=str, required=False)
    post_parser.add_argument('value', type=int, required=True)
    post_parser.add_argument('violation_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                             required=True)
    post_parser.add_argument('notification_id', type=int, required=False)
    post_parser.add_argument('priority', type=int, required=False)

    rule_violation_dao = RuleViolationDAO()

    def post(self):
        """ Method that creates the RuleViolationDTO object according to the data in the body of the Restful request and writes it to the database """

        data = self.post_parser.parse_args()

        try:
            rule_violation_dto = RuleViolationDTO(**data)
            self.rule_violation_dao.save_to_db(rule_violation_dto)
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500

        return rule_violation_dto.serialize, 201

    def put(self):
        """ Method that creates or updates the RuleViolationDTO object according to the data contained in the body of the Restful request """

        data = self.post_parser.parse_args()

        rule_violation_dto = self.rule_violation_dao.find_by_id(data['id'])

        if rule_violation_dto:
            rule_violation_dto.reference_table = data['reference_table']
            rule_violation_dto.reference_id = data['reference_id']
            rule_violation_dto.prediction_id = data['prediction_id']
            rule_violation_dto.rule = data['rule']
            rule_violation_dto.value_source = data['value_source']
            rule_violation_dto.value = data['value']
            rule_violation_dto.violation_date = data['violation_date']
            rule_violation_dto.notification_id = data['notification_id']
            rule_violation_dto.priority = PriorityEnum.get_by_name['priority']

        else:
            rule_violation_dto = RuleViolationDTO(**data)

        self.rule_violation_dao.save_to_db(rule_violation_dto)

        return rule_violation_dto.serialize
