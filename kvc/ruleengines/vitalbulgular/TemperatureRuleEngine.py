from ai.enums.PriorityEnum import PriorityEnum
from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.enums.TemperatureEnum import TemperatureEnum
from kvc.ruleengines.RuleViolationException import RuleViolationException


class TemperatureRuleEngine(AbstractRuleEngine):
    """ """

    def execute(self, islem_no, temperature, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        """ """
        exception_list = []
        if temperature < 36:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Vucut sıcakliği 36 derecenın altına düştü",
                                           TemperatureEnum.DUSUK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahmini vucut sıcakliği 36 derecenın altına düşebilir!",
                                           temperature, TemperatureEnum.DUSUK_ATES, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))

        if 38 < temperature <= 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Vucut sıcakliği 37.5 derecenın üstüne çıktı", TemperatureEnum.YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id, notification_id,
                                           priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahmin vucut sıcakliği 37.5 derecenın üstüne çıkabılır",
                                           TemperatureEnum.YUKSEK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.MEDIUM))

        if temperature > 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Vucut sıcakliği 40 derecenın üstüne çikti", TemperatureEnum.COK_YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id, notification_id,
                                           priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahnmin vucut sıcakliği 40 derecenın üstüne çıkabılır",
                                           TemperatureEnum.COK_YUKSEK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))

        return exception_list
