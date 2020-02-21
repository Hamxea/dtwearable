from datetime import datetime

from ai.aimodels.TemperaturePredictionAIModel import TemperaturePredictionAIModel
from ai.restful.models.RuleViolationDTO import RuleViolationDTO
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
    """Hemşire gözlem servis """

    hemsire_gozlem_dao = HemsireGozlemDAO()
    islem_dao = IslemDAO()
    temperature_rule_engine = TemperatureRuleEngine()
    nabiz_rule_engine = NabizRuleEngine()
    tansiyon_rule_engine = TansiyonRuleEngine()
    rule_violation_service = RuleViolationService()
    prediction_service = PredictionService()

    def create_hemsire_gozlem(self, hemsire_gozlem):
        """ Hemşire gözlem servis ve kural tabanı"""

        try:
            self.hemsire_gozlem_dao.save_to_db(hemsire_gozlem)

            rule_violation_exception_list = []
            rule_violation_exception_list.extend(self.get_temperature_rule_violations(hemsire_gozlem))
            rule_violation_exception_list.extend(self.get_tansiyon_rule_violations(hemsire_gozlem))
            rule_violation_exception_list.extend(self.get_nabiz__rule_violations(hemsire_gozlem))

            self.rule_violation_service.save_rule_violation_and_notifications(rule_violation_exception_list)

        except RuleViolationException as e:
            print(e)
            self.rule_violation_service.save_rule_violations(rule_violation_exception_list)

    """self.sivi_takip_rule_engine.execute(islem_dto=None, sivi_farki=sivi_alimi.sivi_farki, yas=None,
                                                tansiyon_sistolik=None, tansiyon_diastolik=None, choosen_type=None,
                                                reference_table=SiviAlimiDTO.__tablename__, reference_id=sivi_alimi.id,
                                                prediction_id=None, notification_id=None)"""

    def get_nabiz__rule_violations(self, hemsire_gozlem):
        """nabiz kural ihlalleri"""

        nabiz_rule_violation_list = []
        nabiz_rule_violation_list.extend(

            self.nabiz_rule_engine.execute(hemsire_gozlem.islem_dto.islem_no, nabiz=hemsire_gozlem.nabiz,
                                           yas=hemsire_gozlem.islem_dto.yas,
                                           tansiyon_sistolik=hemsire_gozlem.tansiyon_sistolik,
                                           tansiyon_diastolik=hemsire_gozlem.tansiyon_diastolik,
                                           choosen_type=None, reference_table=HemsireGozlemDTO.__tablename__,
                                           reference_id=hemsire_gozlem.id, prediction_id=None, notification_id=None,
                                           priority=None))
        return nabiz_rule_violation_list

    def get_tansiyon_rule_violations(self, hemsire_gozlem):
        """ tansiyon diastolik ve sistolik özellikler kural ihlalleri"""
        tansiyon_rule_violation_list = []
        tansiyon_rule_violation_list.extend(
            self.tansiyon_rule_engine.execute(hemsire_gozlem.islem_dto.islem_no, nabiz=hemsire_gozlem.nabiz,
                                              yas=hemsire_gozlem.islem_dto.yas,
                                              tansiyon_sistolik=hemsire_gozlem.tansiyon_sistolik,
                                              tansiyon_diastolik=hemsire_gozlem.tansiyon_diastolik,
                                              choosen_type=None, reference_table=HemsireGozlemDTO.__tablename__,
                                              reference_id=hemsire_gozlem.id, prediction_id=None, notification_id=None,
                                              priority=None))

        return tansiyon_rule_violation_list

    def get_temperature_rule_violations(self, hemsire_gozlem):
        """Kural motorlar, hem ilk özellik vucut sicakliği hem temperature tahmin eden vucuk sıcaklığı """

        temp_rule_violation_exception_list = []
        temp_rule_violation_exception_list.extend(
            self.temperature_rule_engine.execute(hemsire_gozlem.islem_dto.islem_no,
                                                 temperature=hemsire_gozlem.vucut_sicakligi,
                                                 yas=hemsire_gozlem.islem_dto.yas,
                                                 tansiyon_sistolik=hemsire_gozlem.tansiyon_sistolik,
                                                 tansiyon_diastolik=hemsire_gozlem.tansiyon_diastolik,
                                                 choosen_type=ChoosenTypeEnum.REAL,
                                                 reference_table=HemsireGozlemDTO.__tablename__,
                                                 reference_id=hemsire_gozlem.id, prediction_id=None,
                                                 notification_id=None, priority=None))

        """TODO....modeli yerel makinemde eğit ve yerel kaydetme modeli ile tahmin et 
            ve temperature prediction kural tabanı testlecek
        {
        "message": "An error occurred while inserting the item. ",
        "exception": "[Errno 2] No such file or directory: 'C:\\\\Users\\\\ismet.bahadir\\\\ai_models\\\\ai.aimodels.TemperaturePredictionAIModel.TemperaturePredictionAIModel_1576829259.9437.pickle'"
        """

        """
        # TemperaturePredictionAIModel.__name__
        #prediction_values = self.hemsire_gozlem_dao.get_feature_values_for_prediction(hemsire_gozlem.islem_no,
        #                                                                             column_name="vucut_sicakligi",
        #                                                                              window_size=TemperaturePredictionAIModel.window_size,
        #                                                                             time_interval_in_hours=TemperaturePredictionAIModel.time_interval_in_hours)

        prediction_dto = self.prediction_service.make_prediction(
            ai_model_class="ai.aimodels.TemperaturePredictionAIModel.TemperaturePredictionAIModel",
            reference_table=HemsireGozlemDTO.__tablename__,
            reference_id=hemsire_gozlem.id,
            prediction_input=prediction_values) #try with 1 n_step ---> hemsire_gozlem.vucuk_sicakliği
        temp_rule_violation_exception_list.append(
            self.temperature_rule_engine.execute(hemsire_gozlem.islem_dto, temperature=prediction_dto.prediction_value, choosen_type=ChoosenTypeEnum.PREDICT, yas=hemsire_gozlem.islem_dto.yas,
                                                                        tansiyon_sistolik=hemsire_gozlem.tansiyon_sistolik, tansiyon_diastolik=hemsire_gozlem.tansiyon_diastolik,
                                                                        reference_table=HemsireGozlemDTO.__tablename__, reference_id=hemsire_gozlem.id, prediction_id=None))"""
        return temp_rule_violation_exception_list
