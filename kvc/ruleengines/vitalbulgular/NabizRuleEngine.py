from kvc.ruleengines.enums.NabizEnum import NabizEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException


class NabizRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.researchgate.net%2Fpublication%2F307997435%2Ffigure%2Ftbl1%2FAS%3A671508972175363%401537111623346%2FPulse-rate-by-age-span.png&imgrefurl=https%3A%2F%2Fwww.researchgate.net%2Ffigure%2FPulse-rate-by-age-span_tbl1_307997435&docid=BEpUxeFjRgb26M&tbnid=0PpLSeO3Nk9PSM%3A&vet=10ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA..i&w=466&h=219&bih=979&biw=1920&q=pulse%20rate&ved=0ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA&iact=mrc&uact=8
    """

    def execute(self, islem_dto, nabiz, yas,  tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table, reference_id, prediction_id):
        """ """

        exception_list = []

        """yaş < 1 yıl için"""
        if yas < 1:
            if nabiz < 120:
                exception_list.append(RuleViolationException("Nabiz 120 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 160 < nabiz <= 170:
                exception_list.append(RuleViolationException("Nabiz 160 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 170:
                exception_list.append(RuleViolationException("Nabiz 170 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        """ 1 < yaş <= 2 """
        if 1 < yas <= 2:
            if nabiz < 90:
                exception_list.append(RuleViolationException("Nabiz 90 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 140 < nabiz <= 150:
                exception_list.append(RuleViolationException("Nabiz 140 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 150:
                exception_list.append(RuleViolationException("Nabiz 150 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        """ 2 < yaş <= 5 """
        if 2 < yas <= 5:
            if nabiz < 80:
                exception_list.append(RuleViolationException("Nabiz 80 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 110 < nabiz <= 120:
                exception_list.append(RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 120:
                exception_list.append(RuleViolationException("Nabiz 120 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        """ 5 < yaş <= 12 """
        if 5 < yas <= 12:
            if nabiz < 75:
                exception_list.append(RuleViolationException("Nabiz 75 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 100 < nabiz <= 110:
                exception_list.append(RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 110:
                exception_list.append(RuleViolationException("Nabiz 110 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        """ 12 < yaş <= 18 """
        if 12 < yas <= 18:
            if nabiz < 60:
                exception_list.append(RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 80 < nabiz <= 90:
                exception_list.append(RuleViolationException("Nabiz 80 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 90:
                exception_list.append(RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        """ yaş > 18 """
        if yas > 18:
            if nabiz < 60:
                exception_list.append(RuleViolationException("Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if 90 < nabiz <=100:
                exception_list.append(RuleViolationException("Nabiz 90 derecenın üstüne çikti", NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

            if nabiz > 100:
                exception_list.append(RuleViolationException("Nabiz 100 derecenın üstüne çikti", NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id, prediction_id))

        return exception_list
