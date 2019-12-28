
from ai.restful.services.RuleViolationService import RuleViolationService
from kvc.restful.daos.IslemDAO import IslemDAO
from kvc.restful.daos.SiviAlimiDAO import SiviAlimiDAO
from kvc.restful.models.SiviAlimiDTO import SiviAlimiDTO
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.sivitakipverileri.SiviTakipRuleEngine import SiviTakipRuleEngine


class SiviAlimiService():
    """ """
    """ sivi alimi service"""

    sivi_alimi_dao = SiviAlimiDAO()
    islem_dao = IslemDAO()
    sivi_alimi_rule_engine = SiviTakipRuleEngine()
    sivi_takip_rule_engine = SiviTakipRuleEngine()
    rule_violation_service = RuleViolationService()

    def create_sivi_alimi(self, sivi_alimi):
        """  sivi alimi service"""
        """ sivi alimi service"""

        try:
            rule_violation_exception_list = []
            self.sivi_alimi_dao.save_to_db(sivi_alimi)

            rule_violation_exception_list.extend(self.get_sivi_alimi_rule_violation(sivi_alimi))
            #rule_violation_exception_list.extend(self.get_genel_hasta_durumu_rule_violation(sivi_alimi, hemsire_gozlem))

            self.rule_violation_service.save_rule_violations(rule_violation_exception_list)
        except RuleViolationException as e:
            self.rule_violation_service.save_rule_violation(rule_violation_exception_list)

    def get_genel_hasta_durumu_rule_violation(self, sivi_alimi, hemsire_gozlem):
        """" hastabın genel tahmın hasta durumu kural tabanı """
        """TODO genel tahmin edice kural tabani ekelecek"""

        genel_tahmin_rule_violation_list = []
        # genel_tahmin_rule_violation_list.extend(self.hasta_genel_alimi_rule_enine)

        return genel_tahmin_rule_violation_list

    def get_sivi_alimi_rule_violation(self, sivi_alimi):
        """ sivi farkı kural tabanlı"""

        sivi_alimi_rule_violation_list = []
        sivi_alimi_rule_violation_list.extend(self.sivi_takip_rule_engine.execute(islem_dto=None, sivi_farki=sivi_alimi.sivi_farki, yas=None,
                                                tansiyon_sistolik=None, tansiyon_diastolik=None, choosen_type=None, reference_table=SiviAlimiDTO.__tablename__ ,
                                                                                   reference_id= sivi_alimi.id, prediction_id=None))

        return sivi_alimi_rule_violation_list

