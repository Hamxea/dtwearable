from db import db


class IslemOperasyon(db.Model):
    __tablename__ = "islem_operasyon"

    id = db.Column(db.Integer, primary_key=True)

    islem_id = db.Column(db.Integer, db.ForeignKey('islem.id'))

    operasyon_sut_kodu = db.Column(db.String)
    operasyon_tipi = db.Column(db.Integer)

    def __init__(self, islem_id: int, operasyon_sut_kodu: str, operasyon_tipi: int):
        self.islem_id = islem_id
        self.operasyon_sut_kodu = operasyon_sut_kodu
        self.operasyon_tipi = operasyon_tipi

    @property
    def serialize(self):
        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'operasyon_sut_kodu': self.operasyon_sut_kodu,
            'operasyon_tipi': self.operasyon_tipi
        }
