from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.Islem import Islem

"""
Islem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
"""
class IslemDAO(AbstractDAO):

    # _id değerine göre Islem nesnesini veritabanından getiren metod
    def find_by_id(self, _id:int):
        return Islem.query.filter_by(id=_id).first()

    # islem_no değerine göre Islem nesnesini veritabanından getiren metod
    def find_by_islem_no(self, islem_no:int):
        return Islem.query.filter_by(islem_no=islem_no).first()