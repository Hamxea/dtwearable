from flask_restful import Resource

from ai.restful.daos.RuleViolationDAO import RuleViolationDAO


class RuleViolationResource(Resource):
    """
    Resource class that has methods that take int type id parameter for RuleViolationResource object
     Methods are created to respond to Restful request types
    """

    dao = RuleViolationDAO()

    def get(self, rule_violation_id: int):
        """ Method that returns the RuleViolationDTO information corresponding to the rule_violation_id parameter """

        rule_violation_dto = self.dao.find_by_id(rule_violation_id)
        if not rule_violation_dto:
            return {'message': 'Object Not Found'}, 404
        return rule_violation_dto.serialize, 200

    def delete(self, rule_violation_id: int):
        """ Method that deletes the Notification TO object corresponding to the rule_violation_id parameter """

        rule_violation_dto = self.dao.find_by_id(rule_violation_id)
        if not rule_violation_dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(rule_violation_dto)
        return {'message': 'Object deleted.'}, 200
