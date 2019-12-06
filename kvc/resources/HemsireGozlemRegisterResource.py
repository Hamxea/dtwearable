from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.daos.HemsireGozlemDAO import HemsireGozlemDAO
from kvc.models.HemsireGozlem import HemsireGozlem

class HemsireGozlemRegisterResource(Resource):
    """
    Hemsire Gözlem nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    hemsire_gozlem_post_parser = reqparse.RequestParser()
    hemsire_gozlem_post_parser.add_argument('id',
                                            type=int,
                                            required=False,
                                            )
    hemsire_gozlem_post_parser.add_argument('islem_id',
                                            type=int,
                                            required=False,
                                            )
    hemsire_gozlem_post_parser.add_argument('olcum_tarihi',
                                            type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                                            required=True
                                            )
    hemsire_gozlem_post_parser.add_argument('vucut_sicakligi',
                                            type=float,
                                            required=True,
                                            )
    hemsire_gozlem_post_parser.add_argument('nabiz',
                                            type=int,
                                            required=True,
                                            )
    hemsire_gozlem_post_parser.add_argument('tansiyon_sistolik',
                                            type=int,
                                            required=True
                                            )
    hemsire_gozlem_post_parser.add_argument('tansiyon_diastolik',
                                            type=int,
                                            required=True
                                            )
    hemsire_gozlem_post_parser.add_argument('spo',
                                            type=int,
                                            required=True
                                            )
    hemsire_gozlem_post_parser.add_argument('o2',
                                            type=int,
                                            required=True
                                            )
    hemsire_gozlem_post_parser.add_argument('aspirasyon',
                                            type=int,
                                            required=True
                                   )
    hemsire_gozlem_post_parser.add_argument('kan_transfuzyonu',
                                            type=int,
                                            required=True
                                   )
    hemsire_gozlem_post_parser.add_argument('diren_takibi',
                                            type=int,
                                            required=True
                                   )

    hemsireGozlemDAO = HemsireGozlemDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Hemsire Gözlem nesnesini olusturan ve veritabanına yazan metod """

        data = self.hemsire_gozlem_post_parser.parse_args()

        hemsire_gozlem = HemsireGozlem(**data)

        try:
            self.hemsireGozlemDAO.save_to_db(hemsire_gozlem)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return hemsire_gozlem.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Hemsire Gözlem nesnesini olusturan veya guncelleyen metod """

        data = self.hemsire_gozlem_post_parser.parse_args()

        heemsire_gozlem = self.hemsireGozlemDAO.find_by_id(data['id'])

        if heemsire_gozlem:
            heemsire_gozlem.islem_id = data['islem_id']
            heemsire_gozlem.olcum_tarihi = data['olcum_tarihi']
            heemsire_gozlem.vucut_sicakligi = data['vucut_sicakligi']
            heemsire_gozlem.nabiz = data['nabiz']
            heemsire_gozlem.tansiyon_sistolik = data['tansiyon_sistolik']
            heemsire_gozlem.tansiyon_diastolik = data['tansiyon_diastolik']
            heemsire_gozlem.spo = data['spo']
            heemsire_gozlem.aspirasyon = data['aspirasyon']
            heemsire_gozlem.kan_transfuzyonu = data['kan_transfuzyonu']
            heemsire_gozlem.diren_takibi = data['diren_takibi']
        else:
            heemsire_gozlem = HemsireGozlem(**data)

        self.HemsireGozlemDAO.save_to_db(heemsire_gozlem)

        return heemsire_gozlem.serialize
