from kvc.ruleengines.enums.NabizEnum import NabizEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException


class NabizRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.researchgate.net%2Fpublication%2F307997435%2Ffigure%2Ftbl1%2FAS%3A671508972175363%401537111623346%2FPulse-rate-by-age-span.png&imgrefurl=https%3A%2F%2Fwww.researchgate.net%2Ffigure%2FPulse-rate-by-age-span_tbl1_307997435&docid=BEpUxeFjRgb26M&tbnid=0PpLSeO3Nk9PSM%3A&vet=10ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA..i&w=466&h=219&bih=979&biw=1920&q=pulse%20rate&ved=0ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA&iact=mrc&uact=8
    """

    def execute(self, yas, nabiz):
        """ """

        """yaş < 1 yıl için"""
        if yas < 1:
            if nabiz < 120:
                raise RuleViolationException("Nabiz 120 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 160 <= 170:
                raise RuleViolationException("Nabiz 160 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 170:
                raise RuleViolationException("Nabiz 170 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)

        """ 1 < yaş <= 2 """
        if 1 < yas <= 2:
            if nabiz < 90:
                raise RuleViolationException("Nabiz 90 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 140 or nabiz <= 150:
                raise RuleViolationException("Nabiz 140 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 150:
                raise RuleViolationException("Nabiz 150 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)

        """ 2 < yaş <= 5 """
        if 2 < yas <= 5:
            if nabiz < 80:
                raise RuleViolationException("Nabiz 80 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 110 or nabiz <= 120:
                raise RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 120:
                raise RuleViolationException("Nabiz 120 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)

        """ 5 < yaş <= 12 """
        if 5 < yas <= 12:
            if nabiz < 75:
                raise RuleViolationException("Nabiz 75 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 100 or nabiz <= 110:
                raise RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 110:
                raise RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)

        """ 12 < yaş <= 18 """
        if 12 < yas <= 18:
            if nabiz < 60:
                raise RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 80 or nabiz <= 90:
                raise RuleViolationException("Nabiz 80 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 90:
                raise RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)

        """ yaş > 18 """
        if yas > 18:
            if nabiz < 60:
                raise RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ)

            if nabiz > 90 or nabiz <=100:
                raise RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ)

            if nabiz > 100:
                raise RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ)
