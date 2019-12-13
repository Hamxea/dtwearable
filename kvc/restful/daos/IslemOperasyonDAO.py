from datetime import datetime
from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.IslemOperasyonDTO import IslemOperasyonDTO

class IslemOperasyonDAO(AbstractDAO):
    """ İşlem Operasyon nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(IslemOperasyonDTO)

    def find_by_id(self, _id: int):
        """ _id değerine göre İşlem Operasyon nesnesini veritabanından getiren metod """

        return IslemOperasyonDTO.query.filter_by(id=_id).first()