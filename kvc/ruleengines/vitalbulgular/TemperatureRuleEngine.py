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
                    RuleViolationException(islem_no, "Vücut sıcaklığı 36 derecenın altına düştü",
                                           TemperatureEnum.DUSUK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahmini vücut sıcaklığı 36 derecenın altına düşebilir!",
                                           temperature, TemperatureEnum.DUSUK_ATES, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))

        if 38 < temperature <= 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Vücut sıcaklığı 37.5 derecenın üstüne çıktı", TemperatureEnum.YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id, notification_id,
                                           priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahmin vücut sıcaklığı 37.5 derecenın üstüne çıkabılır",
                                           TemperatureEnum.YUKSEK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.MEDIUM))

        if temperature > 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Vücut sıcaklığı 40 derecenin üstüne çıktı", TemperatureEnum.COK_YUKSEK_ATES,
                                           temperature, reference_table, reference_id, prediction_id, notification_id,
                                           priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahnmin vücut sıcaklığı 40 derecenın üstüne çıkabılır",
                                           TemperatureEnum.COK_YUKSEK_ATES, temperature, reference_table, reference_id,
                                           prediction_id, notification_id, priority=PriorityEnum.HIGH))

        return exception_list
