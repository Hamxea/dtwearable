import json
from datetime import datetime

from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO


class RuleViolationService():
    """ Kural motorundan çıkan kural ihlallerinin veri tabanına kaydının yapıldığı sınıf """

    rule_violation_dao = RuleViolationDAO()


    def save_rule_violation_to_db(self, reference_table, reference_id, prediction_id, rule, value_source, value, violation_date):
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """
        rule_violation_dto = RuleViolationDTO(id=None, reference_table=reference_table, reference_id=reference_id,
                                          prediction_id=prediction_id, rule=rule, value_source=value_source,
                                          value=value, violation_date=violation_date)
        try:
            self.rule_violation_dao.save_to_db(rule_violation_dto)
            return rule_violation_dto
        except Exception as e:
            raise Exception("Error occured while inserting.")
