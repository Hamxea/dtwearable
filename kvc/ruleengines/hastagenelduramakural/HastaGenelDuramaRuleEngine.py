from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.SiviTakipEnum import SiviTakipEnum


class HastaGenelDuramaRuleEngine(AbstractRuleEngine):
    """ TODO..Hasta genel durama gore kural tabanı"""

    def execute(self, islem_dao, sivi_farki, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id):
        """ """
        exception_list = []

        return exception_list
