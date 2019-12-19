from flask_restful import Resource

from ai.restful.daos.RuleViolationDAO import RuleViolationDAO


class RuleViolationResource(Resource):
    """
    RuleViolationResource nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    dao = RuleViolationDAO()

    def get(self, rule_violation_id: int):
        """ rule_violation_id parametresine karsılık gelen RuleViolationDTO bilgisi donen metod """

        rule_violation_dto = self.dao.find_by_id(rule_violation_id)
        if not rule_violation_dto:
            return {'message': 'Object Not Found'}, 404
        return rule_violation_dto.serialize, 200

    def delete(self, rule_violation_id: int):
        """ rule_violation_id parametresine karsılık gelen NotificationDTO nesnesini silen metod """

        rule_violation_dto = self.dao.find_by_id(rule_violation_id)
        if not rule_violation_dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(rule_violation_dto)
        return {'message': 'Object deleted.'}, 200
