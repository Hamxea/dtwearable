from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.SiviTakipEnum import SiviTakipEnum


class SiviTakipRuleEngine(AbstractRuleEngine):
    """https://www.wikizeroo.org/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvRmx1aWRfYmFsYW5jZQ
    Bilgi yer: Oral rehydration therapy Bölum
    """

    def execute(self, islem_dto, sivi_farki, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id):
        """Sivi Alimi Kural tabanı"""

        exception_list = []
        if sivi_farki > 0:
            exception_list.append(RuleViolationException("Sıvı kaybı alınan sıvıdan daha fazla",

                                                         SiviTakipEnum.NEGATIF_SIVI_GENGESI, sivi_farki,
                                                         reference_table,
                                                         reference_id, prediction_id))
        if sivi_farki < 0:
            exception_list.append(RuleViolationException("Alınan sıvı, sıvı kaybından daha büyüktür",
                                                         SiviTakipEnum.POZITIF_SIVI_GENGESI, sivi_farki,
                                                         reference_table,
                                                         reference_id, prediction_id))

        return exception_list
