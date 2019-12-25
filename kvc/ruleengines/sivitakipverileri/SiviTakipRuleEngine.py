from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.SiviTakipEnum import SiviTakipEnum


class SiviTakipRuleEngine(AbstractRuleEngine):
    """https://www.wikizeroo.org/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvRmx1aWRfYmFsYW5jZQ
    Bilgi yer: Oral rehydration therapy Bölum
    """

    def execute(self, islem_dao, sivi_farki):
        """ """

        if sivi_farki > 0:
            raise RuleViolationException("Sıvı kaybı alınan sıvıdan daha fazla", SiviTakipEnum.NEGATIF_SIVI_GENGESI)
        if sivi_farki < 0:
            raise RuleViolationException("Alınan sıvı, sıvı kaybından daha büyüktür", SiviTakipEnum.POZITIF_SIVI_GENGESI)
