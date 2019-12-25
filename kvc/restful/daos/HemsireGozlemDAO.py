from datetime import datetime, timedelta

from sqlalchemy import text

from ai.restful.daos.AbstractDAO import AbstractDAO
from db import db
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

    def get_feature_values_for_prediction(self, islem_no, column_name, window_size, time_interval_in_hours):
        sql_text = text(
            "select :column_name from hemsire_gozlem where islem_no = :islem_no order by olcum_tarihi desc limit :window_size")

        result = db.session.execute(sql_text, {'column_name': column_name, 'islem_no': islem_no,
                                               'window_size': window_size}).fetchall()

        if len(result) < window_size:
            raise Exception("Tahmin için yeterli gözlem bulunmamaktadır")

        for i in range(1, window_size):
            if result.olcum_tarihi[i] - result.olcum_tarihi[i-1] > timedelta(hours=time_interval_in_hours):
                raise Exception("Zaman aralığına uygun yeterli bulunmamaktadır. Window Size: {}, Time Interval: {}".format(window_size, time_interval_in_hours))

        return result
    """def delete_from_db(self, islem_no: int):
        return HemsireGozle."""
