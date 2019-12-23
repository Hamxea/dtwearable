from kvc.ruleengines.enums import NabizEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException

class NabizRuleEngine(AbstractRuleEngine):
    """ """
    def execute(self, yas, nabiz):
        """ """

        """yaş < 1 yıl için"""
        if yas < 1:
            if nabiz < 120:
                raise RuleViolationException("Nabiz 120 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 170:
                raise RuleViolationException("Nabiz 170 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz > 160:
                raise RuleViolationException("Nabiz 160 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)

        """ 1 < yaş <= 2 """
        if yas > 1 and  yas <= 2:
            if nabiz < 90:
                raise RuleViolationException("Nabiz 90 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 150:
                raise RuleViolationException("Nabiz 150 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz >140:
                raise RuleViolationException("Nabiz 140 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)

        """ 2 < yaş <= 5 """
        if yas > 2 and yas <= 5:
            if nabiz < 80:
                raise RuleViolationException("Nabiz 80 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 120:
                raise RuleViolationException("Nabiz 120 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz > 110:
                raise RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)

        """ 5 < yaş <= 12 """
        if yas > 5 and yas <= 12:
            if nabiz < 75:
                raise RuleViolationException("Nabiz 75 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 110:
                raise RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz > 100:
                raise RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)

        """ 12 < yaş <= 18 """
        if yas > 12 and yas <= 18:
            if nabiz < 60:
                raise RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 90:
                raise RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz > 80:
                raise RuleViolationException("Nabiz 80 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)

        """ yaş > 18 """
        if yas > 18:
            if nabiz < 60:
                raise RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_ATES)

            if nabiz > 100:
                raise RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.YUKSEK_ATES)

            if nabiz > 90:
                raise RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_ATES)









