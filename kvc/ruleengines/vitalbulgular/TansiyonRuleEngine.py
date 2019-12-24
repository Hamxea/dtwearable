from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.enums.TansiyonEnum import TansiyonEnum


class TansiyonRuleEngine():
    """ Reference: https://www.health.harvard.edu/heart-health/reading-the-new-blood-pressure-guidelines
    """

    def execute(self, cisiyet, yas, tansiyon_sistolik, tansiyon_diastolik):
        """ """

        if (120 <= tansiyon_sistolik <= 129) and (tansiyon_diastolik < 80):
            raise RuleViolationException("Tansiyon Yükseldi. TANSIYON SİSTOLİK 120 ile 129 arasına çikti "
                                         "ve TANSİYON DİASTOLİK 80 altına düstü", TansiyonEnum.YUKSEK_TANSIYON)

        if (130 <= tansiyon_sistolik <= 139) or (80 <= tansiyon_diastolik <= 89):
            raise RuleViolationException("Tansiyon Yükseldi. HİPERTENSİYON ASAMA-1. "
                                         "TANSİYON SİSTOLİK 130 la 139 arasına çikti "
                                         "ve TANSİYON DİASTOLİK 89 ile 80 arasına çikti", TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_1)

        if (tansiyon_sistolik >= 140) or (tansiyon_diastolik > 90):
            raise RuleViolationException("Tansiyon Yükseldi. HİPERTENSİYON ASAMA-2. "
                                         "TANSİYON SİSTOLİK 140 yükseldi "
                                         "ve TANSİYON DİASTOLİK 90    ", TansiyonEnum.YUKSEK_TANSIYON_HIPERTENSIYON_ASAMA_2)

        if (tansiyon_sistolik >= 180) and (tansiyon_diastolik > 120):
            raise RuleViolationException("Tansiyon Çök Yükseldi. HİPERTENSİF KRİZLER ", TansiyonEnum.HIPERTENSIF_KRIZLER)

        if (tansiyon_sistolik >= 180) or (tansiyon_diastolik > 120):
            raise RuleViolationException("Tansiyon Çök Yükseldi. HİPERTENSİF KRİZLER ", TansiyonEnum.HIPERTENSIF_KRIZLER)

