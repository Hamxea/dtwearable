from datetime import datetime

from flask import request
from flask_restful import reqparse, Resource

from kvc.restful.daos.LabSonucDAO import LabSonucDAO
from kvc.restful.models.LabSonucDTO import LabSonucDTO


class LabSonucBatchRegisterResource(Resource):
    """
    LabSonuc nesnesi için parametre almayan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id', type=int, required=False, action='append')
    post_parser.add_argument('islem_id', type=int, required=True, action='append')
    post_parser.add_argument('lis_kabul_id', type=int, required=True, action='append')
    post_parser.add_argument('numune_tarihi', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(), required=True, action='append')
    post_parser.add_argument('tahlil_kodu', type=str, required=True, action='append')
    post_parser.add_argument('tahlil_deger', type=str, required=True, action='append')

    dao = LabSonucDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan toplu veriye gore LabSonucDTO nesnesini olusturan ve veritabanına yazan metod """

        # TODO liste içinde bulunan nesnenin parse işlemi araştırılacak
        lab_sonuc_list = request.json
        error_message = self.parse_args(lab_sonuc_list)
        if error_message is not None:
            return {"message": error_message}, 500

        result = []
        for lab_sonuc_dto in lab_sonuc_list:
            try:
                dto = LabSonucDTO(id=None,
                                  islem_id=lab_sonuc_dto['islem_id'],
                                  lis_kabul_id=lab_sonuc_dto['lis_kabul_id'],
                                  numune_tarihi=lab_sonuc_dto['numune_tarihi'],
                                  tahlil_kodu=lab_sonuc_dto['tahlil_kodu'],
                                  tahlil_deger=lab_sonuc_dto['tahlil_deger'])
                self.dao.save_to_db(dto)
                result.append(dto.serialize)
            except Exception as e:
                result.append({
                    "object": lab_sonuc_dto,
                    "message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                })

        return result, 201

    def parse_args(self, lab_sonuc_list):
        """ TODO Şu an sadece required kontrolü yapılıyor. reqparse ile doğru yöntem bulunamaz ise tip ve format kontrolü eklenmeli"""

        for lab_sonuc_dto in lab_sonuc_list:
            for argument in self.post_parser.args:
                if argument.required and argument.name not in lab_sonuc_dto:
                    return {argument.name: "Missing required parameter in the JSON body or the post body or the query string"}
