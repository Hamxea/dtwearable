from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.Islem import Islem

class IslemDAO(AbstractDAO):
    """
    Islem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def find_by_id(self, _id:int):
        """ _id değerine göre Islem nesnesini veritabanından getiren metod """

        return Islem.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_no:int):
        """ islem_no değerine göre Islem nesnesini veritabanından getiren metod """

        return Islem.query.filter_by(islem_no=islem_no).first()