from datetime import datetime

from flask_restful import reqparse, Resource
from kvc.restful.daos.IslemOperasyonDAO import IslemOperasyonDAO
from kvc.restful.models.IslemOperasyonDTO import IslemOperasyonDTO

class IslemOperasyonRegisterResource(Resource) :
    """
    Islem Operasyon nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """

    islem_operasyon_post_parser = reqparse.RequestParser()
    islem_operasyon_post_parser.add_argument('id',
                                            type=int,
                                            required=False,
                                            )
    islem_operasyon_post_parser.add_argument('islem_no',
                                            type=int,
                                            required=False,
                                            )
    islem_operasyon_post_parser.add_argument('operasyon_sut',
                                             type=str,
                                             required=False,
                                             )
    islem_operasyon_post_parser.add_argument('operasyon_tipi',
                                             type=int,
                                             required=False,
                                             )
    islemOperasyonDAO = IslemOperasyonDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Operasyon nesnesini olusturan ve veritabanına yazan metod """

        data = self.islem_operasyon_post_parser.parse_args()
        islem_operasyon = IslemOperasyonDTO(**data)
        try:
            self.islemOperasyonDAO.save_to_db(islem_operasyon)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return islem_operasyon.serialize, 201
    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Operasyon nesnesini olusturan veya guncelleyen metod """

        data = self.islem_operasyon_post_parser.parse_args()

        islem_operasyon = self.islemOperasyonDAO.find_by_id(data['id'])
        if islem_operasyon:
            islem_operasyon.islem_no = data['islem_no']
            islem_operasyon.operasyon_sut = data['operasyon_sut']
            islem_operasyon.operasyon_tipi = data['operasyon_tipi']
        else:
            islem_operasyon = IslemOperasyonDTO(**data)

        self.islemOperasyonDAO.save_to_db(islem_operasyon)

        return islem_operasyon.serialize