from datetime import datetime

from ai.restful.services.RuleViolationService import RuleViolationService
from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO
from kvc.restful.daos.IslemDAO import IslemDAO
from kvc.restful.models.HemsireGozlemDTO import HemsireGozlemDTO
from kvc.ruleengines.NabizRuleEngine import NabizRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.TemperatureRuleEngine import TemperatureRuleEngine


class HemsireGozlemService():
    """ """

    hemsire_gozlem_dao = HemsireGozlemDAO()
    islem_dao = IslemDAO()
    temperature_rule_engine = TemperatureRuleEngine()
    nabiz_rule_engine = NabizRuleEngine()
    tansiyon_rule_engine = TansiyonRuleEngine()
    rule_violation_service = RuleViolationService()

    def create_hemsire_gozlem(self, hemsire_gozlem):
        """  """

        try:
            self.hemsire_gozlem_dao.save_to_db(hemsire_gozlem)
            self.temperature_rule_engine.execute(hemsire_gozlem.islem_dto,  hemsire_gozlem.vucut_sicakligi)

        except RuleViolationException as e:
            """ TODO  rule_violation_service düzeltecek...tek db save_to olması lazım"""
            self.rule_violation_service.save_rule_violation_to_db(HemsireGozlemDTO.__tablename__, hemsire_gozlem.id,
                                                                  None, e.rule_enum, None,
                                                                  hemsire_gozlem.vucut_sicakligi, datetime.now())
"""
        try:
            self.nabiz_rule_engine.execute(hemsire_gozlem.islem_dto.yas, hemsire_gozlem.nabiz)
        except RuleViolationException as e2:
            self.rule_violation_service.save_rule_violation_to_db(HemsireGozlemDTO.__tablename__, hemsire_gozlem.id,
                                                                  None, e2.rule_enum.name, None,
                                                                  hemsire_gozlem.nabiz, datetime.now())
"""
