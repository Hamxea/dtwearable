from datetime import datetime

from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.HemsireGozlem import HemsireGozlem


class HemsireGozlemDAO(AbstractDAO):
    """ Hemsire Gözlem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def find_by_id(self, _id: int):
        """ _id değerine göre Hemşire Gözlem nesnesini veritabanından getiren metod """

        return HemsireGozlem.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_no: int):
        """ islem_no değerine göre Hemşire Gözlem nesnesini veritabanından getiren metod """

        return HemsireGozlem.query.filter_by(islem_no=islem_no).first()

    def get_fever_in_date_range(self, start_date: datetime, end_date: datetime):
        """ Belirli tarihler arasındaki ates bilgilerini dönen metod"""

        if end_date <= start_date:
            raise Exception("end_date ({}) cannot be earlier than start_date ({})".format(end_date, start_date))

        result = HemsireGozlem.query.filter(HemsireGozlem.olcum_tarihi >= start_date,
                                   HemsireGozlem.olcum_tarihi <= end_date).all()
        return result

    """def delete_from_db(self, islem_no: int):
        return HemsireGozle."""
