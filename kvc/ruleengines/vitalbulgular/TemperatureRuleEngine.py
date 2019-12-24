from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.enums.TemperatureEnum import TemperatureEnum
from kvc.ruleengines.RuleViolationException import RuleViolationException


class TemperatureRuleEngine(AbstractRuleEngine):
    """ """

    def execute(self, islem_dto, temperature):
        """ """
        if temperature < 36:
            raise RuleViolationException("Vucut sıcakliği 36 derecenın altına düştü", TemperatureEnum.DUSUK_ATES)

        if temperature > 38 or temperature <= 40:
            raise RuleViolationException("Vucut sıcakliği 37.5 derecenın üstüne çikti", TemperatureEnum.YUKSEK_ATES)

        if temperature > 40:
            raise RuleViolationException("Vucut sıcakliği 40 derecenın üstüne çikti", TemperatureEnum.COK_YUKSEK_ATES)
