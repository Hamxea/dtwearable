from datetime import datetime

from ai.aimodels.TemperaturePredictionAIModel import TemperaturePredictionAIModel
from ai.restful.services.PredictionService import PredictionService
from ai.restful.services.RuleViolationService import RuleViolationService
from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO
from kvc.restful.daos.IslemDAO import IslemDAO
from kvc.restful.models.HemsireGozlemDTO import HemsireGozlemDTO
from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.vitalbulgular.NabizRuleEngine import NabizRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.vitalbulgular.TansiyonRuleEngine import TansiyonRuleEngine
from kvc.ruleengines.vitalbulgular.TemperatureRuleEngine import TemperatureRuleEngine


class HemsireGozlemService():
    """ """

    hemsire_gozlem_dao = HemsireGozlemDAO()
    islem_dao = IslemDAO()
    temperature_rule_engine = TemperatureRuleEngine()
    nabiz_rule_engine = NabizRuleEngine()
    tansiyon_rule_engine = TansiyonRuleEngine()
    rule_violation_service = RuleViolationService()
    prediction_service = PredictionService()

    def create_hemsire_gozlem(self, hemsire_gozlem):
        """  """

        try:
            self.hemsire_gozlem_dao.save_to_db(hemsire_gozlem)

            rule_violation_exception_list = []
            rule_violation_exception_list.extend(self.get_temperature_rule_violations(hemsire_gozlem))

            self.rule_violation_service.save_rule_violations(rule_violation_list=rule_violation_exception_list)

        except RuleViolationException as e:
            """ TODO  rule_violation_service düzeltecek...tek db save_to olması lazım"""
            self.rule_violation_service.save_rule_violation_to_db(HemsireGozlemDTO.__tablename__, hemsire_gozlem.id,
                                                                  None, e.rule_enum.name, None,
                                                                  hemsire_gozlem.vucut_sicakligi, datetime.now())

    def get_temperature_rule_violations(self, hemsire_gozlem):
        temp_rule_violation_exception_list = []
        temp_rule_violation_exception_list.extend(
            self.temperature_rule_engine.execute(hemsire_gozlem.islem_dto, hemsire_gozlem.vucut_sicakligi,
                                                 choosen_type=ChoosenTypeEnum.REAL))

        # TemperaturePredictionAIModel.__name__
        prediction_values = self.hemsire_gozlem_dao.get_feature_values_for_prediction(hemsire_gozlem.islem_no,
                                                                                      column_name="vucut_sicakligi",
                                                                                      window_size=TemperaturePredictionAIModel.window_size,
                                                                                      time_interval_in_hours=TemperaturePredictionAIModel.time_interval_in_hours)

        prediction_dto = self.prediction_service.make_prediction(
            ai_model_class="ai.aimodels.TemperaturePredictionAIModel.TemperaturePredictionAIModel",
            reference_table=HemsireGozlemDTO.__tablename__,
            reference_id=hemsire_gozlem.id,
            prediction_input=prediction_values)
        temp_rule_violation_exception_list.append(
            self.temperature_rule_engine.execute(hemsire_gozlem.islem_dto, prediction_dto.prediction_value,
                                                 ChoosenTypeEnum.PREDICT))

        return temp_rule_violation_exception_list



"""
        try:
            self.nabiz_rule_engine.execute(hemsire_gozlem.islem_dto.yas, hemsire_gozlem.nabiz)
        except RuleViolationException as e2:
            self.rule_violation_service.save_rule_violation_to_db(HemsireGozlemDTO.__tablename__, hemsire_gozlem.id,
                                                                  None, e2.rule_enum.name, None,
                                                                  hemsire_gozlem.nabiz, datetime.now())
"""
