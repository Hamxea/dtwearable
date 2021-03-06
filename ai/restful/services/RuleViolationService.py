import logging
from datetime import datetime

from ai.restful.daos.NotificationDAO import NotificationDAO
from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.NotificationDTO import NotificationDTO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO

from dt.ruleengines.RuleViolationException import RuleViolationException


class RuleViolationService():
    """ class in which rule violations from the rule engine are saved in the database """

    rule_violation_dao = RuleViolationDAO()
    notification_dao = NotificationDAO()

    def save_rule_violation_and_notifications(self, rule_violation_list):
        """ results from the rule engine are sent to the database in case of violation.
                                                         method that allows registration and sending notifications"""

        for i in range(0, 3):
            # range 0 dan 2'ye kadar, LOW priority (0), MEDIUM priority (1), ve HIGH priority (2)
            new_rule_violation_list = []
            try:
                for rule_violation_exception in rule_violation_list:
                    if rule_violation_exception.priority == i:
                        new_rule_violation_list.append(rule_violation_exception)

                if not new_rule_violation_list:
                    pass
                else:
                    notification_dto = self.save_notification(new_rule_violation_list)
                    self.save_rule_violation(notification_dto, new_rule_violation_list)
            except Exception as e:
                logging.exception(e, exc_info=True)

    def save_notification(self, new_violation_list):
        global violation

        try:
            #TODO save notification to db
            return
        except Exception as e:
            logging.exception(e, exc_info=True)

    def save_rule_violation(self, notification_dto, rule_violation_list):

        for rule_violation_exception in rule_violation_list:
            self.save_rule_violation_to_db(rule_violation_exception.reference_table,
                                           rule_violation_exception.reference_id,
                                           rule_violation_exception.prediction_id,
                                           rule_violation_exception.rule_enum.name,
                                           rule_violation_exception.message,
                                           rule_violation_exception.value,
                                           datetime.now(),
                                           notification_dto.id,
                                           notification_dto.priority)

    def save_rule_violation_to_db(self, reference_table, reference_id, prediction_id, rule, value_source, value,
                                  violation_date, notification_id, priority):
        """ method that records the results from the rule engine to the database in case of violation """
        rule_violation_dto = RuleViolationDTO(id=None,
                                              reference_table=reference_table,
                                              reference_id=reference_id,
                                              prediction_id=prediction_id,
                                              rule=rule,
                                              value_source=value_source,
                                              value=value,
                                              violation_date=violation_date,
                                              notification_id=notification_id,
                                              priority=priority)

        try:
            self.rule_violation_dao.save_to_db(rule_violation_dto)

            return rule_violation_dto
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Error occurred while inserting.")

    def save_rule_violations(self, rule_violation_exception: RuleViolationException):
        """ """

    def save_notfication_to_db(self, staff_id, priority, message, notification_date, error_message, islem_no):
        """ method that records the results from the rule engine to the database in case of violation """

        notification_dto = NotificationDTO(id=None,
                                           staff_id=staff_id,
                                           priority=priority,
                                           message=message,
                                           notification_date=notification_date,
                                           error_message=error_message)
        try:
            self.notification_dao.save_to_db(notification_dto)
            # emit('message', notification_dto.serialize, broadcast=True, namespace='/')
            # self.hbys_notification_integration_service.send_notification_via_socket(notification_message=notification_dto.serialize)

            # TODO  # Change the notification parameter to report_dto (add actionNo).
            #              # And also add the send_notification_to_hbys function to NotificationRegisterResource class


            return notification_dto

        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Error occurred while inserting.")
