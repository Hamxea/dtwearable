from ai.enums.PriorityEnum import PriorityEnum
from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.SiviTakipEnum import SiviTakipEnum


class SiviTakipRuleEngine(AbstractRuleEngine):
    """https://www.wikizeroo.org/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvRmx1aWRfYmFsYW5jZQ
    Bilgi yer: Oral rehydration therapy Bölum
    """

    def execute(self, islem_no, sivi_farki, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        """Sivi Alimi Kural tabanı"""

        exception_list = []
        if sivi_farki > 0:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException(islem_no, "Sıvı kaybı alınan sıvıdan daha fazla",
                                                             SiviTakipEnum.NEGATIF_SIVI_GENGESI, sivi_farki,
                                                             reference_table, reference_id, prediction_id,
                                                             notification_id,
                                                             priority=PriorityEnum.HIGH))
            else:
                exception_list.append(RuleViolationException(islem_no, "Tahmini Sıvı kaybı alınan sıvıdan daha fazla",
                                                             SiviTakipEnum.NEGATIF_SIVI_GENGESI, sivi_farki,
                                                             reference_table, reference_id, prediction_id,
                                                             notification_id,
                                                             priority=PriorityEnum.HIGH))

        elif sivi_farki < 0:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException(islem_no, "Alınan sıvı, sıvı kaybından daha büyüktür",
                                                             SiviTakipEnum.POZITIF_SIVI_GENGESI, sivi_farki,
                                                             reference_table, reference_id, prediction_id,
                                                             notification_id,
                                                             priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tahmini Alınan sıvı, sıvı kaybından daha büyüktür",
                                           SiviTakipEnum.POZITIF_SIVI_GENGESI, sivi_farki, reference_table,
                                           reference_id, prediction_id, notification_id, priority=PriorityEnum.MEDIUM))

        return exception_list
