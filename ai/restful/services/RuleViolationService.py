from datetime import datetime

import requests
from flask_socketio import emit

from ai.enums.PriorityEnum import PriorityEnum
from ai.restful.daos.NotificationDAO import NotificationDAO
from ai.restful.daos.RuleViolationDAO import RuleViolationDAO
from ai.restful.models.NotificationDTO import NotificationDTO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO
from kvc.ruleengines.RuleViolationException import RuleViolationException


class RuleViolationService():
    """ Kural motorundan çıkan kural ihlallerinin veri tabanına kaydının yapıldığı sınıf """

    rule_violation_dao = RuleViolationDAO()
    notification_dao = NotificationDAO()

    def save_rule_violations(self, rule_violation_list):
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """

        for rule_violation_exception in rule_violation_list:
            try:
                self.save_rule_violation(rule_violation_exception)

            except Exception as e:
                print(e)

    def save_rule_violation(self, rule_violation_exception: RuleViolationException):
        self.save_rule_violation_to_db(rule_violation_exception.reference_table,
                                       rule_violation_exception.reference_id,
                                       rule_violation_exception.prediction_id,
                                       rule_violation_exception.rule_enum.name,
                                       rule_violation_exception.message,
                                       rule_violation_exception.value,
                                       datetime.now())

    def save_rule_violation_to_db(self, reference_table, reference_id, prediction_id, rule, value_source, value,
                                  violation_date):
        """ Kural motorundan çıkan sonuçların, ihlal olması durumunda veri tabanına kaydını sağlayan metot """
        rule_violation_dto = RuleViolationDTO(id=None,
                                              reference_table=reference_table,
                                              reference_id=reference_id,
                                              prediction_id=prediction_id,
                                              rule=rule,
                                              value_source=value_source,
                                              value=value,
                                              violation_date=violation_date)

        self.save_notfication_to_db(rule_violation_id=rule_violation_dto.id, staff_id=None,
                                    priority=PriorityEnum.HIGH, message=rule_violation_dto.value_source,
                                    notification_date=datetime.now(), error_message=rule_violation_dto.value_source)

        try:
            self.rule_violation_dao.save_to_db(rule_violation_dto)

            return rule_violation_dto
        except Exception as e:
            print(e)
            raise Exception("Error occurred while inserting.")

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
            # emit('message', notification_dto.serialize, broadcast=True, namespace='/')
            self.send_notification_via_socket(notification_message=notification_dto.serialize)

            # TODO  # Bildirim parametresini report_dto olarak değiştirin (actionNo ekle).
            #  Ve ayrıca, send_notification_to_hbys işlevini NotificationRegisterResource sınıfına ekleyin
            #  {
            #   'islemNO:......
            # 	"rule_violation_id": 105,
            # 	"staff_id": 77,
            # 	"priority": "LOW",
            # 	"message": " cfdfsa Test message",
            # 	"notification_date": "18.01.2020 00:00:00",
            # 	"error_message": "ghvgc notification error."
            # }
            test_notification = {"islemNo": 3004160431, "message": "Hata Oluştu...."}
            self.send_notification_to_hbys(notification_dict=test_notification)
            return notification_dto
        except Exception as e:
            print(e)
            raise Exception("Error occurred while inserting.")

    def send_notification_via_socket(self, notification_message):
        """ socket üzeeride bildirim gönder"""
        emit('message', notification_message, broadcast=True, namespace='/')
        return

    def send_notification_to_hbys(self, notification_dict):
        """HBYS bildirimlerin anlık gönderilmesi"""

        url = 'http://10.6.0.55:8080/hbys-rs/hbys/Interaktif/InteraktifDuyuru/keyMindNotification'

        # create session hbys login
        session, jwt_auth, hazelcast_session_id, j_session_id = self.hbys_login_auth()

        # send notification to hbys
        headers_send_hbys = {'JWTAuth': jwt_auth, 'Content-Type': 'application/json',
                             'Cookie': 'hazelcast.sessionId=' + hazelcast_session_id + '; JSESSIONID=' + j_session_id}
        send_hby_response = session.post(url, json=notification_dict, headers=headers_send_hbys)
        print('Send response from server', send_hby_response)
        dict_from_server = send_hby_response.json()
        print(dict_from_server)

        # clear session and logout
        self.hbys_logout(session=session, jwt_auth=jwt_auth)

        return send_hby_response

    def hbys_login_auth(self):
        """ hbys sunucusundan "cookies" ve "headers" alın ve hbys'e giriş yapın """

        login_cred = {"kullaniciAdi": "ENTEGRASYON", "sifre": "keydata06", "locale": "tr-TR", "organizasyon": 21}
        headers_login = {'Content-Type': 'application/json'}
        url = 'http://10.6.0.55:8080/hbys-rs/hbys/HBYSSistem/KullaniciGiris/login'

        try:
            with requests.Session() as session:
                login_resp = session.post(url=url, json=login_cred, headers=headers_login)

                print('login response from server', login_resp)
                dict_from_server = login_resp.json()
                print(dict_from_server)
                # get JWTAuth token
                jwt_auth = dict_from_server['data']['JWTAuth']
                # hazelcast.sessionId and JSESSIONID cookies from the server by using a requests Session object
                hazelcast_session_id = session.cookies['hazelcast.sessionId']
                j_session_id = session.cookies['JSESSIONID']

        except requests.exceptions.HTTPError as e:
            print("Http Error:", e)
        except requests.exceptions.ConnectionError as er:
            print("Error Connecting:", er)
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
        except requests.exceptions.RequestException as error:
            print("OOps: Something Else", error)

        return session, jwt_auth, hazelcast_session_id, j_session_id

    def hbys_logout(self, session, jwt_auth):
        """Clear sessşon and Hbys logout"""

        headers = {'JWTAuth': jwt_auth}
        url = 'http://10.6.0.55:8080/hbys-rs/hbys/Sistem/KullaniciGiris/logout'

        logout_resp = session.get(url, headers=headers)

        print('logout response from server', logout_resp)
        dict_from_server = logout_resp.json()
        print(dict_from_server)
        return logout_resp
