from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.IslemTani import IslemTani

class IslemTaniDAO(AbstractDAO):
    """
    Islem Tani nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def find_by_id(self, _id:int) -> IslemTani:
        """ _id değerine göre IslemTani nesnesini veritabanından getiren metod """

        return IslemTani.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_id:int) -> IslemTani:
        """ islem_id değerine göre IslemTani nesnesini veritabanından getiren metod """

        return IslemTani.query.filter_by(islem_id=islem_id).first()
