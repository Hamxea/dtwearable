import datetime

from db import db

class HemsireGozlem(db.Model):
    """ Hemşire Gözlem tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "hemsire_gozlem"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_id = db.Column(db.BigInteger)
    olcum_tarihi = db.Column(db.DateTime)
    vucut_sicakligi = db.Column(db.Float)
    nabiz = db.Column(db.Integer)
    tansiyon_sistolik = db.Column(db.Integer)
    tansiyon_diastolik = db.Column(db.Integer)
    spo = db.Column(db.Integer)
    o2 = db.Column(db.Integer)
    aspirasyon = db.Column(db.Boolean)
    kan_transfuzyonu = db.Column(db.Integer)
    diren_takibi = db.Column(db.Boolean)

    def __init__(self, id: int, islem_id: int, olcum_tarihi: datetime, vucut_sicakligi: float, nabiz: int,
                 tansiyon_sistolik: int, tansiyon_diastolik: int, spo: int, o2: int, aspirasyon: float,
                 kan_transfuzyonu: int, diren_takibi: int):

        self.id = id
        self.islem_id = islem_id
        self.olcum_tarihi = olcum_tarihi
        self.vucut_sicakligi = vucut_sicakligi
        self.nabiz = nabiz
        self.tansiyon_diastolik = tansiyon_diastolik
        self.tansiyon_sistolik = tansiyon_sistolik
        self.spo = spo
        self.o2 = o2
        self.aspirasyon = aspirasyon
        self.kan_transfuzyonu = kan_transfuzyonu
        self.diren_takibi = diren_takibi


    @property
    def serialize(self):
        """ Hemşire Gözlem nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'olcum_tarihi': self.olcum_tarihi,
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
