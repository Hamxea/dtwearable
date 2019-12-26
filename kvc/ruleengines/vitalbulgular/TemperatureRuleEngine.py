from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.enums.TemperatureEnum import TemperatureEnum
from kvc.ruleengines.RuleViolationException import RuleViolationException


class TemperatureRuleEngine(AbstractRuleEngine):
    """ """

    def execute(self, islem_dto, temperature, choosen_type):
        """ """

        exception_list = []
        if temperature < 36:
            if choosen_type == ChoosenTypeEnum.REAL:
                raise RuleViolationException("Vucut sıcakliği 36 derecenın altına düştü", TemperatureEnum.DUSUK_ATES,
                       temperature)
            else:
                raise RuleViolationException("Tahmini vucut sıcakliği 36 derecenın altına düşebilir!",
                       temperature, TemperatureEnum.DUSUK_ATES)

        elif 38 < temperature <= 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                raise RuleViolationException("Vucut sıcakliği 37.5 derecenın üstüne çıktı", TemperatureEnum.YUKSEK_ATES,
                       temperature)
            else:
                raise RuleViolationException("Tahmin vucut sıcakliği 37.5 derecenın üstüne çıkabılır",
                                              TemperatureEnum.YUKSEK_ATES,
                                              temperature)

        elif temperature > 40:
            if choosen_type == ChoosenTypeEnum.REAL:
                raise RuleViolationException("Vucut sıcakliği 40 derecenın üstüne çikti", TemperatureEnum.COK_YUKSEK_ATES,
                       temperature)
            else:
                raise RuleViolationException("Tahnmin vucut sıcakliği 40 derecenın üstüne çıkabılır", TemperatureEnum.COK_YUKSEK_ATES,
                       temperature)

        return exception_list
