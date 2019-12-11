from datetime import datetime
from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.IslemOperasyon import IslemOperasyon

class IslemOperasyonDAO(AbstractDAO):
    """ İşlem Operasyon nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """
    def find_by_id(self, _id: int):
        """ _id değerine göre İşlem Operasyon nesnesini veritabanından getiren metod """

        return IslemOperasyon.query.filter_by(id=_id).first()