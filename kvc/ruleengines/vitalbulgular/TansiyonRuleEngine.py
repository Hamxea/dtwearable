from ai.enums.PriorityEnum import PriorityEnum
from kvc.restful.services.ChoosenTypeEnum import ChoosenTypeEnum
from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.TansiyonEnum import TansiyonEnum


class TansiyonRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.health.harvard.edu/heart-health/reading-the-new-blood-pressure-guidelines
    """

    def execute(self, islem_no, nabiz, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        """ """

        exception_list = []

        if 120 <= tansiyon_sistolik <= 129 and tansiyon_diastolik < 80:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Yükseldi: "
                                                     "TANSIYON SİSTOLİK 120 ile 129 arasına çıktı "
                                                     "ve TANSİYON DİASTOLİK 80 altına düstü",
                                           TansiyonEnum.YUKSEK_TANSIYON, tansiyon_sistolik, reference_table,
                                           reference_id,
                                           prediction_id,
                                           notification_id, priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Yükselebilir: "
                                                     "TANSIYON SİSTOLİK 120 ile 129 arasına çıkabılır "
                                                     "ve TANSİYON DİASTOLİK 80 altına düsebilir",
                                           TansiyonEnum.YUKSEK_TANSIYON, tansiyon_sistolik, reference_table,
                                           reference_id,
                                           prediction_id,
                                           notification_id, priority=PriorityEnum.MEDIUM))

        elif 130 <= tansiyon_sistolik <= 139 or 80 <= tansiyon_diastolik <= 89:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException(islem_no, "Tansiyon Yükseldi: "
                                                                       "TANSİYON SİSTOLİK 130 la 139 arasına çıktı "
                                                                       "veya TANSİYON DİASTOLİK 89 ile 80 arasına çıktı "
                                                                       "(HİPERTENSİYON ASAMA-1)",
                                                             TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_1,
                                                             tansiyon_sistolik, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(RuleViolationException(islem_no, "Tansiyon Yükselebilir: "
                                                                       "TANSİYON SİSTOLİK 130 la 139 arasına çıkabılır"
                                                                       "veya TANSİYON DİASTOLİK 89 ile 80 arasına çıkabılır"
                                                                       "(HİPERTENSİYON ASAMA-1)",
                                                             TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_1,
                                                             tansiyon_sistolik, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))

        elif tansiyon_sistolik >= 140 or tansiyon_diastolik > 90:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException(islem_no, "Tansiyon Yükseldi: "
                                                                       "TANSİYON SİSTOLİK 140 üstüne yükseldi "
                                                                       "veya TANSİYON DİASTOLİK 90 üstüne yükseldi "
                                                                       "(HİPERTENSİYON ASAMA-2).",
                                                             TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_2,
                                                             tansiyon_sistolik, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.HIGH))
            else:
                exception_list.append(RuleViolationException(islem_no, "Tansiyon Yükselebilir: "
                                                                       "TANSİYON SİSTOLİK 130 la 139 arasına çıkabılır "
                                                                       "veya TANSİYON DİASTOLİK 89 ile 80 arasına çıkabılır "
                                                                       "(HİPERTENSİYON ASAMA-1)",
                                                             TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_1,
                                                             tansiyon_sistolik, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))

        elif tansiyon_sistolik >= 180 and tansiyon_diastolik > 120:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Çok Yükseldi: "
                                                     "TANSİYON SİSTOLİK 180 üstüne yükseldi "
                                                     "ve TANSİYON DİASTOLİK 120 üstüne yükseldi "
                                                     "(HİPERTENSİF KRİZLER)",
                                           TansiyonEnum.HIPERTENSIF_KRIZLER,
                                           tansiyon_sistolik, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Çok Yükselebilir: "
                                                     "TANSİYON SİSTOLİK 180 üstüne yükselebilir "
                                                     "ve TANSİYON DİASTOLİK 120 üstüne Yükselebilir "
                                                     "(HİPERTENSİF KRİZLER)",
                                           TansiyonEnum.HIPERTENSIF_KRIZLER,
                                           tansiyon_sistolik, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))

        elif tansiyon_sistolik >= 180 or tansiyon_diastolik > 120:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Çok Yükseldi: "
                                                     "TANSİYON SİSTOLİK 180 üstüne yükseldi "
                                                     "veya TANSİYON DİASTOLİK 120 üstüne yükseldi "
                                                     "(HİPERTENSİF KRİZLER)",
                                           TansiyonEnum.HIPERTENSIF_KRIZLER,
                                           tansiyon_sistolik, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException(islem_no, "Tansiyon Çok Yükselebilir: "
                                                     "TANSİYON SİSTOLİK 180 üstüne Yükselebilir "
                                                     "veya TANSİYON DİASTOLİK 120 üstüne Yükselebilir "
                                                     "(HİPERTENSİF KRİZLER)",
                                           TansiyonEnum.HIPERTENSIF_KRIZLER,
                                           tansiyon_sistolik, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))

        return exception_list
