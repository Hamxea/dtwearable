import datetime

from ai.restful.services.RuleViolationService import RuleViolationService
from kvc.restful.daos.IslemDAO import IslemDAO
from kvc.restful.daos.SiviAlimiDAO import SiviAlimiDAO
from kvc.restful.models.SiviAlimiDTO import SiviAlimiDTO
from kvc.ruleengines.RuleViolationException import RuleViolationException
from kvc.ruleengines.sivitakipverileri import SiviTakipRuleEngine


class SiviAlimiService():
    """ """

    sivi_alimi_dao = SiviAlimiDAO()
    islem_dao = IslemDAO()
    sivi_alimi_rule_engine = SiviTakipRuleEngine()
    rule_violation_service = RuleViolationService()

    def create_hemsire_gozlem(self, sivi_alimi):
        """  """

        try:
            self.sivi_alimi_dao.save_to_db(sivi_alimi)
            self.sivi_alimi_rule_engine.execute(sivi_alimi.islem_dto, sivi_alimi.sivi_farki)

        except RuleViolationException as e:
            self.rule_violation_service.save_rule_violation_to_db(SiviAlimiDTO.__tablename__, sivi_alimi.id,
                                                                  None, e.rule_enum.name, None,
                                                                  sivi_alimi.vucut_sicakligi, datetime.now())
