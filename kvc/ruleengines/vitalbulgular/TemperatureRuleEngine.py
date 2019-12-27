from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.enums.TemperatureEnum import TemperatureEnum
from kvc.ruleengines.RuleViolationException import RuleViolationException


class TemperatureRuleEngine(AbstractRuleEngine):
    """ """

    def execute(self, islem_dto, temperature, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table, reference_id, prediction_id):
        """ """
        exception_list = []
        if temperature < 36:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("Vucut sıcakliği 36 derecenın altına düştü",
                                           TemperatureEnum.DUSUK_ATES, temperature, reference_table, reference_id, prediction_id))
            else:
                exception_list.append(
                    RuleViolationException("Tahmini vucut sıcakliği 36 derecenın altına düşebilir!",
                                           temperature, TemperatureEnum.DUSUK_ATES, reference_table, reference_id, prediction_id))

        elif 38 < temperature <= 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("Vucut sıcakliği 37.5 derecenın üstüne çıktı", TemperatureEnum.YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id))
            else:
                exception_list.append(
                    RuleViolationException("Tahmin vucut sıcakliği 37.5 derecenın üstüne çıkabılır", TemperatureEnum.YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id))

        if temperature > 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("Vucut sıcakliği 40 derecenın üstüne çikti", TemperatureEnum.COK_YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id))
            else:
                exception_list.append(
                    RuleViolationException("Tahnmin vucut sıcakliği 40 derecenın üstüne çıkabılır", TemperatureEnum.COK_YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id))

        return exception_list
