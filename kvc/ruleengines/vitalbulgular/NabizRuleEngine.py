from ai.enums.PriorityEnum import PriorityEnum
from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.enums.NabizEnum import NabizEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException


class NabizRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.researchgate.net%2Fpublication%2F307997435%2Ffigure%2Ftbl1%2FAS%3A671508972175363%401537111623346%2FPulse-rate-by-age-span.png&imgrefurl=https%3A%2F%2Fwww.researchgate.net%2Ffigure%2FPulse-rate-by-age-span_tbl1_307997435&docid=BEpUxeFjRgb26M&tbnid=0PpLSeO3Nk9PSM%3A&vet=10ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA..i&w=466&h=219&bih=979&biw=1920&q=pulse%20rate&ved=0ahUKEwiBxf-5w8TmAhUJjqQKHXvIDUsQMwh5KAQwBA&iact=mrc&uact=8
    """

    def execute(self, islem_no, nabiz, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        """ """

        exception_list = []

        """yaş < 1 yıl için"""
        if yas < 1:
            if nabiz < 120:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 120 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 120 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id,
                                               prediction_id, notification_id, priority=PriorityEnum.HIGH))

            elif 160 < nabiz <= 170:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 160 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 160 derecenın üstüne çıktabılır",
                                               NabizEnum.YUKSEK_NABIZ, nabiz, reference_table, reference_id,
                                               prediction_id, notification_id, priority=PriorityEnum.MEDIUM))

            elif nabiz > 170:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 170 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 170 derecenın üstüne çıktabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ, nabiz, reference_table, reference_id,
                                               prediction_id, notification_id, priority=PriorityEnum.HIGH))

        """ 1 < yaş <= 2 """
        if 1 < yas <= 2:
            if nabiz < 90:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 90 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 90 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ, nabiz, reference_table, reference_id,
                                               prediction_id, notification_id, priority=PriorityEnum.HIGH))

            elif 140 < nabiz <= 150:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 140 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 140 derecenın üstüne çıkabılır",
                                               NabizEnum.YUKSEK_NABIZ, nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))

            elif nabiz > 150:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 150 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 150 derecenın üstüne çıkabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

        """ 2 < yaş <= 5 """
        if 2 < yas <= 5:
            if nabiz < 80:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 80 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 80 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

            elif 110 < nabiz <= 120:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 110 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 110 derecenın üstüne çıktabılır",
                                               NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))

            elif nabiz > 120:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 120 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 120 derecenın üstüne çıktabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

        """ 5 < yaş <= 12 """
        if 5 < yas <= 12:
            if nabiz < 75:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 75 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 75 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

            elif 100 < nabiz <= 110:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 100 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 100 derecenın üstüne çıktabılır",
                                               NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))

            elif nabiz > 110:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 110 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 110 derecenın üstüne çıktabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

        """ 12 < yaş <= 18 """
        if 12 < yas <= 18:
            if nabiz < 60:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini sNabiz 60 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

            elif 80 < nabiz <= 90:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 80 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahnmin Nabiz 80 derecenın üstüne çıktabılır",
                                               NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))

            elif nabiz > 90:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 90 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 90 derecenın üstüne çıkabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

        """ yaş > 18 """
        if yas > 18:
            if nabiz < 60:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 60 derecenın altına düştü", NabizEnum.DUSUK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 60 derecenın altına düşebilir",
                                               NabizEnum.DUSUK_NABIZ, nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

            elif 90 < nabiz <= 100:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 90 derecenın üstüne çıktı", NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 90 derecenın üstüne çıkabılır",
                                               NabizEnum.YUKSEK_NABIZ,
                                               nabiz,
                                               reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.MEDIUM))

            elif nabiz > 100:
                if choosen_type == ChoosenTypeEnum.REAL:
                    exception_list.append(
                        RuleViolationException(islem_no, "Nabiz 100 derecenın üstüne çıktı", NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))
                else:
                    exception_list.append(
                        RuleViolationException(islem_no, "Tahmini Nabiz 100 derecenın üstüne çıkabılır",
                                               NabizEnum.COK_YUKSEK_NABIZ,
                                               nabiz, reference_table, reference_id, prediction_id, notification_id,
                                               priority=PriorityEnum.HIGH))

        return exception_list