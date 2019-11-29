from datetime import datetime

from flask_restful import reqparse, Resource

from kvc.daos.HemsireGozlemDAO import HemsireGozlemDAO
from kvc.daos.IslemDAO import IslemDAO
from kvc.models.HemsireGozlem import HemsireGozlem


class HemsireGozlemRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=False)
    parser.add_argument('islem_no', type=int, required=False)
    parser.add_argument('islem_id', type=int, required=False)
    parser.add_argument('olcum_tarihi', type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(), required=True)
    parser.add_argument('vucut_sicakligi', type=float, required=False)
    parser.add_argument('nabiz', type=int, required=False)
    parser.add_argument('tansiyon_sistolik', type=int, required=False)
    parser.add_argument('tansiyon_diastolik', type=int, required=False)
    parser.add_argument('spo', type=int, required=False)
    parser.add_argument('o2', type=int, required=False)
    parser.add_argument('aspirasyon', type=bool, required=False)
    parser.add_argument('kan_transfuzyonu', type=bool, required=False)
    parser.add_argument('diren_takibi', type=bool, required=False)

    hemsireGozlemDAO = HemsireGozlemDAO()
    islemDAO = IslemDAO()

    def post(self):
        data = self.parser.parse_args()

        islem = self.islemDAO.find_by_islem_no(data['islem_no'])
        if islem is None:
            return {'message': 'Islem not found! islem_no: {}'.format(data['islem_no'])}, 404

        hemsire_gozlem = HemsireGozlem(
            id=data['id'],
            islem_id=islem.id,
            olcum_tarihi=data['olcum_tarihi'],
            vucut_sicakligi=data['vucut_sicakligi'],
            nabiz=data['nabiz'],
            tansiyon_sistolik=data['tansiyon_sistolik'],
            tansiyon_diastolik=data['tansiyon_diastolik'],
            spo=data['spo'],
            o2=data['o2'],
            aspirasyon=data['aspirasyon'],
            kan_transfuzyonu=data['kan_transfuzyonu'],
            diren_takibi=data['diren_takibi'])

        try:
            self.hemsireGozlemDAO.save_to_db(hemsire_gozlem)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return hemsire_gozlem.serialize, 201

    def put(self):
        data = self.parser.parse_args()

        hemsire_gozlem = self.hemsireGozlemDAO.find_by_id(data['id'])

        islem = self.islemDAO.find_by_islem_no(data['islem_no'])
        if islem is None:
            return {'message': 'Islem not found! islem_no: {}'.format(data['islem_no'])}, 404

        if hemsire_gozlem:
            hemsire_gozlem.islem_id = data['islem_id']
            hemsire_gozlem.olcum_tarihi = data['olcum_tarihi']
            hemsire_gozlem.vucut_sicakligi = data['vucut_sicakligi']
            hemsire_gozlem.nabiz = data['nabiz']
            hemsire_gozlem.tansiyon_sistolik = data['tansiyon_sistolik']
            hemsire_gozlem.tansiyon_diastolik = data['tansiyon_diastolik']
            hemsire_gozlem.spo = data['spo']
            hemsire_gozlem.o2 = data['o2']
            hemsire_gozlem.aspirasyon = data['aspirasyon']
            hemsire_gozlem.kan_transfuzyonu = data['kan_transfuzyonu']
            hemsire_gozlem.diren_takibi = data['diren_takibi']
        else:
            hemsire_gozlem = HemsireGozlem(
                id=data['id'],
                islem_id=islem.id,
                olcum_tarihi=data['olcum_tarihi'],
                vucut_sicakligi=data['vucut_sicakligi'],
                nabiz=data['nabiz'],
                tansiyon_sistolik=data['tansiyon_sistolik'],
                tansiyon_diastolik=data['tansiyon_diastolik'],
                spo=data['spo'],
                o2=data['o2'],
                aspirasyon=data['aspirasyon'],
                kan_transfuzyonu=data['kan_transfuzyonu'],
                diren_takibi=data['diren_takibi'])

        self.hemsireGozlemDAO.save_to_db(hemsire_gozlem)

        return hemsire_gozlem.serialize
