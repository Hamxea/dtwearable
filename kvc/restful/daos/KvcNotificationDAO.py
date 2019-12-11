from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.KvcNotificationDTO import KvcNotificationDTO


class KvcNotificationDAO(AbstractDAO):
    """ KvcNotification nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(KvcNotificationDTO)

    def get_by_islem_no(self, islem_no_list):
        """ islem_no değerlerine göre KvcNotification nesnelerini dönen metod """

        return None
        # return KvcNotificationDTO.query.filter_by(islem_no=islem_no).first()