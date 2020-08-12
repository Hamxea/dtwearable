import logging
from datetime import datetime

from ai.restful.daos.NotificationDAO import NotificationDAO
from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.NotificationDTO import NotificationDTO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO
from kvc.restful.services.HbysNotificationIntegrationService import HbysNotificationIntegrationService
from kvc.ruleengines.RuleViolationException import RuleViolationException


class RuleViolationService():
    """ Kural motorundan çıkan kural ihlallerinin veri tabanına kaydının yapıldığı sınıf """

    rule_violation_dao = RuleViolationDAO()
    notification_dao = NotificationDAO()
    hbys_notification_integration_service = HbysNotificationIntegrationService()

    def save_rule_violation_and_notifications(self, rule_violation_list):
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına
                                                            kaydını ve bildirim gönderme sağlayan metot """

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
        hasta_adi = "{HASTA_ADI} isimli hasta için uyarı oluştu.\n"
        birim = "Birim no = {BIRIM_ADI}\n"
        yatak = "Yatak no = {YATAK_NO}\n"
        notication_message = ""

        for violation in new_violation_list:
            notication_message += "* " + violation.message + "\n"
        try:
            notification_dto = self.save_notfication_to_db(staff_id=None, priority=violation.priority,
                                                           message=hasta_adi + notication_message,
                                                           notification_date=datetime.now(),
                                                           error_message=hasta_adi + notication_message + birim + yatak,
                                                           islem_no=violation.islem_no)
            return notification_dto
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
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """
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
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """

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

            # TODO  # Bildirim parametresini report_dto olarak değiştirin (actionNo ekle).
            #  Ve ayrıca, send_notification_to_hbys işlevini NotificationRegisterResource sınıfına ekleyin
            #  {
            #   'islemNO:.....
            # 	"staff_id": 77,
            # 	"priority": "LOW",
            # 	"message": " cfdfsa Test message {HASTA_ADI} {BIRIM_ADI} {YATAK_NO}",
            # 	"notification_date": "18.01.2020 00:00:00",
            # 	"error_message": "ghvgc notification error."
            # }
            test_notification = {"islemNo": 3004160431, "message": "Hata Oluştu...."}
            notification_message = {"islemNo": islem_no, "message": notification_dto.message}
            self.hbys_notification_integration_service.send_notification_to_hbys(notification_dict=notification_message)
            return notification_dto

        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Error occurred while inserting.")
