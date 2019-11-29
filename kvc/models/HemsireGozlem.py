import datetime

from db import db


class HemsireGozlem(db.Model):
    __tablename__ = "hemsire_gozlem"

    id = db.Column(db.Integer, primary_key=True)
    islem_id = db.Column(db.Integer, db.ForeignKey('islem.id'))
    olcum_tarihi = db.Column(db.DateTime)
    vucut_sicakligi = db.Column(db.Float)
    nabiz = db.Column(db.SmallInteger)
    tansiyon_sistolik = db.Column(db.SmallInteger)
    tansiyon_diastolik = db.Column(db.SmallInteger)
    spo = db.Column(db.SmallInteger)
    o2 = db.Column(db.SmallInteger)
    aspirasyon = db.Column(db.Boolean)
    kan_transfuzyonu = db.Column(db.Boolean)
    diren_takibi = db.Column(db.Boolean)

    def __init__(self, id: int,
                 islem_id: int,
                 olcum_tarihi: datetime,
                 vucut_sicakligi: float,
                 nabiz: int,
                 tansiyon_sistolik: int,
                 tansiyon_diastolik: int,
                 spo: int,
                 o2: int,
                 aspirasyon: bool,
                 kan_transfuzyonu: bool,
                 diren_takibi: bool):
        self.id = id
        self.islem_id = islem_id
        self.olcum_tarihi = olcum_tarihi
        self.vucut_sicakligi = vucut_sicakligi
        self.nabiz = nabiz
        self.tansiyon_sistolik = tansiyon_sistolik
        self.tansiyon_diastolik = tansiyon_diastolik
        self.spo = spo
        self.o2 = o2
        self.aspirasyon = aspirasyon
        self.kan_transfuzyonu = kan_transfuzyonu
        self.diren_takibi = diren_takibi

    @property
    def serialize(self):
        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'olcum_tarihi': self.olcum_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'vucut_sicakligi': self.vucut_sicakligi,
            'nabiz': self.nabiz,
            'tansiyon_sistolik': self.tansiyon_sistolik,
            'tansiyon_diastolik': self.tansiyon_diastolik,
            'spo': self.spo,
            'o2': self.o2,
            'aspirasyon': self.aspirasyon,
            'kan_transfuzyonu': self.kan_transfuzyonu,
            'diren_takibi': self.diren_takibi
        }
