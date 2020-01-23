from ai.restful.daos.NotificationDAO import NotificationDAO
from ai.restful.models.NotificationDTO import NotificationDTO


class NotificationService():
    """ """

    notification_dao = NotificationDAO

    def save_notfication_to_db(self, rule_violation_id, staff_id, priority, message, notification_date, error_message):
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """
        notification_dto = NotificationDTO(id=None,
                                              rule_violation_id=rule_violation_id,
                                              staff_id=staff_id,
                                              priority=priority,
                                              message=message,
                                              notification_date=notification_date,
                                              error_message=error_message)
        try:
            self.notification_dao.save_to_db(notification_dto)
            return notification_dto
        except Exception as e:
            print(e)
            raise Exception("Error occured while inserting.")

