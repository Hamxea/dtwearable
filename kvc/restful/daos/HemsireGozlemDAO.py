from datetime import datetime

from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.HemsireGozlemDTO import HemsireGozlemDTO


class HemsireGozlemDAO(AbstractDAO):
    """ Hemsire Gözlem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(HemsireGozlemDTO)

    def find_by_islem_no(self, islem_no: int):
        """ islem_no değerine göre Hemşire Gözlem nesnesini veritabanından getiren metod """

        return HemsireGozlemDTO.query.filter_by(islem_no=islem_no).first()

    def get_temperature_in_date_range(self, start_date: datetime, end_date: datetime):
        """ Belirli tarihler arasındaki ates bilgilerini dönen metod"""

        if end_date <= start_date:
            raise Exception("end_date ({}) cannot be earlier than start_date ({})".format(end_date, start_date))

        result = HemsireGozlemDTO.query.filter(HemsireGozlemDTO.olcum_tarihi >= start_date,
                                               HemsireGozlemDTO.olcum_tarihi <= end_date).all()
        return result

    """def delete_from_db(self, islem_no: int):
        return HemsireGozle."""
