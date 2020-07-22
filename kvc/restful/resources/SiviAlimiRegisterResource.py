from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.restful.daos.SiviAlimiDAO import SiviAlimiDAO
from kvc.restful.models.SiviAlimiDTO import SiviAlimiDTO
from kvc.restful.services.SiviAlimiService import SiviAlimiService


class SiviAlimiRegisterResource(Resource):
    """
    Sıvı Alımı nesnesi için parametre almayan metodları barındıran Register Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    """ Restful isteklerini tanımlamak için oluşturulur, uyumsuzluk halinde hata dönmesi sağlanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('id',
                             type=int,
                             required=False,
                             )
    post_parser.add_argument('islem_no',
                             type=int,
                             required=True,
                             )
    post_parser.add_argument('olcum_tarihi',
                             type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                             required=True
                             )
    post_parser.add_argument('kilo',
                             type=float,
                             required=True,
                             )
    post_parser.add_argument('aldigi_sivi_miktari_oral',
                             type=float,
                             required=True,
                             )
    post_parser.add_argument('aldigi_sivi_miktari_intravanoz',
                             type=float,
                             required=True,
                             )
    post_parser.add_argument('aldigi_sivi_miktari_nazogastrik',
                             type=float,
                             required=True
                             )
    post_parser.add_argument('cikardigi_sivi_miktari_idrar',
                             type=float,
                             required=False
                             )
    post_parser.add_argument('cikardigi_sivi_miktari_nazogastrik',
                             type=float,
                             required=False
                             )
    post_parser.add_argument('cikardigi_sivi_diren',
                             type=float,
                             required=False
                             )
    post_parser.add_argument('sivi_farki',
                             type=float,
                             required=False
                             )

    siviAlimiDAO = SiviAlimiDAO()
    sivi_alimi_service = SiviAlimiService()
    def post(self):
        """ Restful isteğinin body kısmındaki veriye gore Sıvı Alımı nesnesini olusturan ve veritabanına yazan metod """

        data = self.post_parser.parse_args()

        try:
            sivi_alimi = SiviAlimiDTO(**data)
            self.sivi_alimi_service.create_sivi_alimi(sivi_alimi)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return sivi_alimi.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmındaki veriye gore Sıvı Alımı nesnesini oluşturan veya güncelleyen metod """

        data = self.post_parser.parse_args()

        sivi_alimi = self.siviAlimiDAO.find_by_id(data['id'])

        if sivi_alimi:
            sivi_alimi.islem_no = data['islem_no']
            sivi_alimi.olcum_tarihi = data['olcum_tarihi']
            sivi_alimi.kilo = data['kilo']
            sivi_alimi.aldigi_sivi_miktari_oral = data['aldigi_sivi_miktari_oral']
            sivi_alimi.aldigi_sivi_miktari_intravanoz = data['aldigi_sivi_miktari_intravanoz']
            sivi_alimi.aldigi_sivi_miktari_nazogastrik = data['aldigi_sivi_miktari_nazogastrik']
            sivi_alimi.cikardigi_sivi_miktari_idrar = data['cikardigi_sivi_miktari_idrar']
            sivi_alimi.cikardigi_sivi_miktari_nazogastrik = data['cikardigi_sivi_miktari_nazogastrik']
            sivi_alimi.cikardigi_sivi_diren = data['cikardigi_sivi_diren']
            sivi_alimi.sivi_farki = data['sivi_farki']
        else:
            sivi_alimi = SiviAlimiDTO(**data)

        self.sivi_alimi_service.create_sivi_alimi(sivi_alimi)

        return sivi_alimi.serialize
