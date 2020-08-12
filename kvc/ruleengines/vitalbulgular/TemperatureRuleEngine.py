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
                    RuleViolationException(islem_no=islem_no, message="Vücut sıcaklığı 36 derecenın altına düştü",
                                           rule_enum=TemperatureEnum.DUSUK_ATES, value=temperature,
                                           reference_table=reference_table, reference_id=reference_id,
                                           prediction_id=prediction_id, notification_id=notification_id,
                                           priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no=islem_no,
                                           message="Tahmini vücut sıcaklığı 36 derecenın altına düşebilir!",
                                           value=temperature, rule_enum=TemperatureEnum.DUSUK_ATES,
                                           reference_table=reference_table, reference_id=reference_id,
                                           prediction_id=prediction_id, notification_id=notification_id,
                                           priority=PriorityEnum.HIGH))

        elif 38 < temperature <= 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no=islem_no, message="Vücut sıcaklığı 37.5 derecenın üstüne çıktı",
                                           rule_enum=TemperatureEnum.YUKSEK_ATES,
                                           value=temperature, reference_table=reference_table,
                                           reference_id=reference_id, prediction_id=prediction_id,
                                           notification_id=notification_id, priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException(islem_no=islem_no,
                                           message="Tahmin vücut sıcaklığı 37.5 derecenın üstüne çıkabılır",
                                           rule_enum=TemperatureEnum.YUKSEK_ATES, value=temperature,
                                           reference_table=reference_table, reference_id=reference_id,
                                           prediction_id=prediction_id, notification_id=notification_id,
                                           priority=PriorityEnum.MEDIUM))

        elif temperature > 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no=islem_no, message="Vücut sıcaklığı 40 derecenin üstüne çıktı",
                                           rule_enum= TemperatureEnum.COK_YUKSEK_ATES, value=temperature,
                                           reference_table=reference_table, reference_id=reference_id,
                                           prediction_id=prediction_id, notification_id=notification_id,
                                           priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no=islem_no, message="Tahnmin vücut sıcaklığı 40 derecenın üstüne çıkabılır",
                                           rule_enum=TemperatureEnum.COK_YUKSEK_ATES, value=temperature,
                                           reference_table=reference_table, reference_id=reference_id,
                                           prediction_id=prediction_id, notification_id=notification_id,
                                           priority=PriorityEnum.HIGH))

        return exception_list
