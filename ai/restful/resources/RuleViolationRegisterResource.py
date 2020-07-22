from datetime import datetime

from flask_restful import reqparse, Resource

from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO


class RuleViolationRegisterResource(Resource):
    """
    RuleViolationDTO nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False)
    post_parser.add_argument('reference_table', type=str, required=True)
    post_parser.add_argument('reference_id', type=int, required=True)
    post_parser.add_argument('prediction_id', type=int, required=True)
    post_parser.add_argument('rule', type=str, required=True)
    post_parser.add_argument('value_source', type=str, required=False)
    post_parser.add_argument('value', type=int, required=True)
    post_parser.add_argument('violation_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(), required=True)


    rule_violation_dao = RuleViolationDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore RuleViolationDTO nesnesini olusturan ve veritabanına yazan metod """

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
        """ Restful isteğinin body kısmında bulunan veriye gore RuleViolationDTO nesnesini olusturan veya guncelleyen metod """

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

        else:
            rule_violation_dto = RuleViolationDTO(**data)

        self.rule_violation_dao.save_to_db(rule_violation_dto)

        return rule_violation_dto.serialize
