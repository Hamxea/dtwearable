from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.restful.daos.IslemDAO import IslemDAO
from kvc.restful.models.IslemDTO import IslemDTO
from kvc.restful.models.enums.CinsiyetEnum import CinsiyetEnum
from kvc.restful.models.enums.KVCLabelEnum import KVCLabelEnum


class IslemRegisterResource(Resource):
    """
    Islem nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    islem_post_parser = reqparse.RequestParser()
    islem_post_parser.add_argument('id',
                                   type=int,
                                   required=False,
                                   )
    islem_post_parser.add_argument('islem_no',
                                   type=int,
                                   required=True,
                                   )
    islem_post_parser.add_argument('kayit_tarihi',
                                   type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                                   required=True
                                   )
    islem_post_parser.add_argument('cinsiyet',
                                   type=str,
                                   required=True,
                                   )
    islem_post_parser.add_argument('yas',
                                   type=int,
                                   required=True,
                                   )
    islem_post_parser.add_argument('operasyon_tarihi',
                                   type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                                   required=True,
                                   )
    islem_post_parser.add_argument('cikis_tarihi',
                                   type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                                   required=True
                                   )
    islem_post_parser.add_argument('etiket',
                                   type=str,
                                   required=False
                                   )
    # islem_parser.add_argument('islem_operasyon_list',
    #                           action='append',
    #                           required=False
    #                           )

    islemDAO = IslemDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem nesnesini olusturan ve veritabanına yazan metod """

        data = self.islem_post_parser.parse_args()

        islem = IslemDTO(None, data['islem_no'], data['kayit_tarihi'], CinsiyetEnum.get_by_name(data['cinsiyet']),
                         data['yas'], data['operasyon_tarihi'], data['cikis_tarihi'], KVCLabelEnum.get_by_name(data['etiket']))

        try:
            self.islemDAO.save_to_db(islem)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return islem.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem nesnesini olusturan veya guncelleyen metod """

        data = self.islem_post_parser.parse_args()

        islem = self.islemDAO.find_by_id(data['id'])

        if islem:
            islem.islem_no = data['islem_no']
            islem.kayit_tarihi = data['kayit_tarihi']
            islem.cinsiyet = CinsiyetEnum.get_by_name(data['cinsiyet'])
            islem.yas = data['yas']
            islem.operasyon_tarihi = data['operasyon_tarihi']
            islem.cikis_tarihi = data['cikis_tarihi']
            islem.etiket = KVCLabelEnum.get_by_name(data['etiket'])
        else:
            islem = IslemDTO(**data)

        self.islemDAO.save_to_db(islem)

        return islem.serialize, 201
