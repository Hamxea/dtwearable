from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.HemsireGozlem import HemsireGozlem


class HemsireGozlemDAO(AbstractDAO):
    """ Sıvı Alımı nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def find_by_id(self, _id: int):
        """ _id değerine göre Hemşire Gözlem nesnesini veritabanından getiren metod """

        return HemsireGozlem.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_no: int):
        """ islem_no değerine göre Hemşire Gözlem nesnesini veritabanından getiren metod """

        return HemsireGozlem.query.filter_by(islem_no=islem_no).first()

    """def delete_from_db(self, islem_no: int):
        return HemsireGozle."""
