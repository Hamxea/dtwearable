from builtins import str

from flask_restful import reqparse, Resource

from kvc.restful.daos.IslemTaniDAO import IslemTaniDAO
from kvc.restful.models.IslemTani import IslemTani

class IslemTaniRegisterResource(Resource):
    """
    Islem Tani nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    islemTani_post_parser = reqparse.RequestParser()
    islemTani_post_parser.add_argument('id',
                                   type=int,
                                   required=False,
                                   )
    islemTani_post_parser.add_argument('islem_id',
                                   type=int,
                                   required=True,
                                   )
    islemTani_post_parser.add_argument('tani_kodu',
                                   type=str,
                                   required=True,
                                   )
    islemTani_post_parser.add_argument('tani_tipi',
                                   type=int,
                                   required=True,
                                   )


    islemTaniDAO = IslemTaniDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Tani nesnesini olusturan ve veritabanına yazan metod """

        data = self.islemTani_post_parser.parse_args()

        islemTani = IslemTani(**data)

        try:
            self.islemTaniDAO.save_to_db(islemTani)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return islemTani.serialize, 201


    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Tani nesnesini olusturan veya guncelleyen metod """

        data = self.islemTani_post_parser.parse_args()

        islemTani = self.islemTaniDAO.find_by_id(data['id'])

        if islemTani:
            islemTani.islem_id = data['islem_id']
            islemTani.tani_kodu = data['tani_kodu']
            islemTani.tani_tipi = data['tani_tipi']
        else:
            islemTani = IslemTani(**data)

        self.islemTaniDAO.save_to_db(islemTani)

        return islemTani.serialize, 201
