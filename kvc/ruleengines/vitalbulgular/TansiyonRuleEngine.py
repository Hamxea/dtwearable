from kvc.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.TansiyonEnum import TansiyonEnum


class TansiyonRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.health.harvard.edu/heart-health/reading-the-new-blood-pressure-guidelines
    """

    def execute(self, islem_dto, nabiz, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table, reference_id, prediction_id):
        """ """

        exception_list = []


        if (120 <= tansiyon_sistolik <= 129) and (tansiyon_diastolik < 80):
            exception_list.append(RuleViolationException("Tansiyon Yükseldi. TANSIYON SİSTOLİK 120 ile 129 arasına çikti "
                                         "ve TANSİYON DİASTOLİK 80 altına düstü", TansiyonEnum.YUKSEK_TANSIYON, tansiyon_sistolik,
                                           reference_table, reference_id, prediction_id))

        if (130 <= tansiyon_sistolik <= 139) or (80 <= tansiyon_diastolik <= 89):
            exception_list.append(RuleViolationException("Tansiyon Yükseldi. HİPERTENSİYON ASAMA-1. "
                                         "TANSİYON SİSTOLİK 130 la 139 arasına çikti "
                                         "ve TANSİYON DİASTOLİK 89 ile 80 arasına çikti", TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_1, tansiyon_sistolik,
                                           reference_table, reference_id, prediction_id))

        if (tansiyon_sistolik >= 140) or (tansiyon_diastolik > 90):
            exception_list.append(RuleViolationException("Tansiyon Yükseldi. HİPERTENSİYON ASAMA-2. "
                                         "TANSİYON SİSTOLİK 140 yükseldi "
                                         "ve TANSİYON DİASTOLİK 90    ", TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_2, tansiyon_sistolik,
                                           reference_table, reference_id, prediction_id))

        if (tansiyon_sistolik >= 180) and (tansiyon_diastolik > 120):
            exception_list.append(RuleViolationException("Tansiyon Çök Yükseldi. HİPERTENSİF KRİZLER ", TansiyonEnum.HIPERTENSIF_KRIZLER, tansiyon_sistolik,
                                           reference_table, reference_id, prediction_id))

        if (tansiyon_sistolik >= 180) or (tansiyon_diastolik > 120):
            exception_list.append(RuleViolationException("Tansiyon Çök Yükseldi. HİPERTENSİF KRİZLER ", TansiyonEnum.HIPERTENSIF_KRIZLER, tansiyon_sistolik,
                                           reference_table, reference_id, prediction_id))

        return exception_list
