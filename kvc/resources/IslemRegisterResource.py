from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.daos.IslemDAO import IslemDAO
from kvc.models.Islem import Islem


class IslemRegisterResource(Resource):
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
                                   type=int,
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
                                   type=int,
                                   required=False
                                   )
    # islem_parser.add_argument('islem_operasyon_list',
    #                           action='append',
    #                           required=False
    #                           )

    islemDAO = IslemDAO()

    def post(self):
        data = self.islem_post_parser.parse_args()

        islem = Islem(**data)

        try:
            self.islemDAO.save_to_db(islem)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return islem.serialize, 201

    def put(self):
        data = self.islem_post_parser.parse_args()

        islem = self.islemDAO.find_by_id(data['id'])

        if islem:
            islem.islem_no = data['islem_no']
            islem.kayit_tarihi = data['kayit_tarihi']
            islem.cinsiyet = data['cinsiyet']
            islem.yas = data['yas']
            islem.operasyon_tarihi = data['operasyon_tarihi']
            islem.cikis_tarihi = data['cikis_tarihi']
            islem.etiket = data['etiket']
        else:
            islem = Islem(**data)

        self.islemDAO.save_to_db(islem)

        return islem.serialize
