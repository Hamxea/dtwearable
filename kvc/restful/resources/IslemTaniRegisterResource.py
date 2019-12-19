from builtins import str

from flask_restful import reqparse, Resource

from kvc.restful.daos.IslemTaniDAO import IslemTaniDAO
from kvc.restful.models.IslemTaniDTO import IslemTaniDTO
from kvc.restful.models.enums.TaniTipiEnum import TaniTipiEnum


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
    islemTani_post_parser.add_argument('islem_no',
                                   type=int,
                                   required=True,
                                   )
    islemTani_post_parser.add_argument('tani_kodu',
                                   type=str,
                                   required=True,
                                   )
    islemTani_post_parser.add_argument('tani_tipi',
                                   type=str,
                                   required=True,
                                   )

    islemTaniDAO = IslemTaniDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Tani nesnesini olusturan ve veritabanına yazan metod """

        data = self.islemTani_post_parser.parse_args()

        islem_tani = IslemTaniDTO(**data)

        try:
            islem_tani = IslemTaniDTO(None, data['islem_id'], data['tani_kodu'],
                                      TaniTipiEnum.get_by_name(data['tani_tipi']))
            self.islemTaniDAO.save_to_db(islem_tani)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500

        return islem_tani.serialize, 201


    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem Tani nesnesini olusturan veya guncelleyen metod """

        data = self.islemTani_post_parser.parse_args()

        islem_tani = self.islemTaniDAO.find_by_id(data['id'])

        if islem_tani:
            islem_tani.islem_no = data['islem_no']
            islem_tani.tani_kodu = data['tani_kodu']
            islem_tani.tani_tipi = data['tani_tipi']
        else:
            islem_tani = IslemTaniDTO(**data)

        self.islemTaniDAO.save_to_db(islem_tani)

        return islem_tani.serialize, 201
