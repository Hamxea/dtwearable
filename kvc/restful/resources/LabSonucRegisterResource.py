from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.restful.daos.LabSonucDAO import LabSonucDAO
from kvc.restful.models.LabSonucDTO import LabSonucDTO


class LabSonucRegisterResource(Resource):
    """
    LabSonuc nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False)
    post_parser.add_argument('islem_no', type=int, required=True)
    post_parser.add_argument('lis_kabul_id', type=int, required=True)
    post_parser.add_argument('numune_tarihi', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(), required=True)
    post_parser.add_argument('tahlil_kodu', type=str, required=True)
    post_parser.add_argument('tahlil_deger', type=str, required=True)

    dao = LabSonucDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore LabSonucDTO nesnesini olusturan ve veritabanına yazan metod """

        data = self.post_parser.parse_args()

        dto = LabSonucDTO(**data)

        try:
            self.dao.save_to_db(dto)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return dto.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore LabSonucDTO nesnesini olusturan veya guncelleyen metod """

        data = self.post_parser.parse_args()

        lab_sonuc_dto = self.dao.find_by_id(data['id'])

        if lab_sonuc_dto:
            lab_sonuc_dto.islem_no = data['islem_no']
            lab_sonuc_dto.lis_kabul_id = data['lis_kabul_id']
            lab_sonuc_dto.numune_tarihi = data['numune_tarihi']
            lab_sonuc_dto.tahlil_kodu = data['tahlil_kodu']
            lab_sonuc_dto.tahlil_deger = data['tahlil_deger']
        else:
            lab_sonuc_dto = LabSonucDTO(**data)

        self.dao.save_to_db(lab_sonuc_dto)

        return lab_sonuc_dto.serialize
