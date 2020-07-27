import logging
import time

import requests
from flask_socketio import emit


class HbysNotificationIntegrationService():
    """Bildirimler hbys entegrasyon Service """

    def send_notification_via_socket(self, notification_message):
        """ socket üzeeride bildirim gönder"""
        emit('message', notification_message, broadcast=True, namespace='/keymind/kvc')
        return

    def send_notification_to_hbys(self, notification_dict):
        """HBYS bildirimlerin anlık gönderilmesi"""

        #https://hbyspreprod.keydata.com.tr/hbys-rs/hbys/Interaktif/InteraktifMesaj/keyMindNotification
        #http://10.6.0.48:8080/hbys-rs/hbys/Interaktif/InteraktifMesaj/keyMindNotification
        url = 'https://hbyspreprod.keydata.com.tr/hbys-rs/hbys/Interaktif/InteraktifMesaj/keyMindNotification'

        # create session hbys login
        session, jwt_auth, hazelcast_session_id, j_session_id = self.hbys_login_auth()

        # send notification to hbys
        headers_send_hbys = {'JWTAuth': jwt_auth, 'Content-Type': 'application/json',
                             'Cookie': 'hazelcast.sessionId=' + hazelcast_session_id + '; JSESSIONID=' + j_session_id}
        send_hby_response = session.post(url, json=notification_dict, headers=headers_send_hbys)
        print('Send response from server', send_hby_response)
        dict_from_server = send_hby_response.json()
        print(dict_from_server)
        print(type(dict_from_server))
        notification_to_lcd = dict_from_server
        self.send_notification_via_socket(notification_message=notification_to_lcd)

        # Delays for 4 seconds.
        time.sleep(4)

        # clear session and logout
        self.hbys_logout(session=session, jwt_auth=jwt_auth)

        return send_hby_response

    def hbys_login_auth(self):
        """ hbys sunucusundan "cookies" ve "headers" alın ve hbys'e giriş yapın """

        # DİLSADT/dilsad92
        login_cred = {"kullaniciAdi": "ENTEGRASYON", "sifre": "keydata06", "locale": "tr-TR", "organizasyon": 21}
        headers_login = {'Content-Type': 'application/json'}
        url = 'https://hbyspreprod.keydata.com.tr/hbys-rs/hbys/HBYSSistem/KullaniciGiris/login'

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
            #print("Http Error:", e)
            logging.exception(e, exc_info=True)
        except requests.exceptions.ConnectionError as er:
            #print("Error Connecting:", er)
            logging.exception(er, exc_info=True)
        except requests.exceptions.Timeout as err:
            #print("Timeout Error:", err)
            logging.exception(err, exc_info=True)
        except requests.exceptions.RequestException as error:
            #print("OOps: Something Else", error)
            logging.exception(error, exc_info=True)

        return session, jwt_auth, hazelcast_session_id, j_session_id

    def hbys_logout(self, session, jwt_auth):
        """Clear sessşon and Hbys logout"""

        headers = {'JWTAuth': jwt_auth}
        url = 'https://hbyspreprod.keydata.com.tr/hbys-rs/hbys/Sistem/KullaniciGiris/logout'

        logout_resp = session.get(url, headers=headers)

        print('logout response from server', logout_resp)
        dict_from_server = logout_resp.json()
        print(dict_from_server)
        return logout_resp
