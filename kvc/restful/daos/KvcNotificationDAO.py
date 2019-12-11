from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.KvcNotificationDTO import KvcNotificationDTO


class KvcNotificationDAO(AbstractDAO):
    """ KvcNotification nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(KvcNotificationDTO)

