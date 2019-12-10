from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models import Islem

class IslemDAO(AbstractDAO):
    """
    Islem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def find_by_id(self, _id:int) -> Islem:
        """ _id değerine göre Islem nesnesini veritabanından getiren metod """

        return Islem.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_no:int) -> Islem:
        """ islem_no değerine göre Islem nesnesini veritabanından getiren metod """

        return Islem.query.filter_by(islem_no=islem_no).first()