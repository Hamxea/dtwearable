from datetime import datetime

from db import db


class LabSonucDTO(db.Model):
    """ Laboratuvar Sonuçları tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "lab_sonuc"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_no = db.Column(db.BigInteger)
    lis_kabul_id = db.Column(db.BigInteger)
    numune_tarihi = db.Column(db.DateTime)
    tahlil_kodu = db.Column(db.String)
    tahlil_deger = db.Column(db.String)

    def __init__(self, id: int, islem_no: int, lis_kabul_id:int, numune_tarihi: datetime, tahlil_kodu: str, tahlil_deger:str):
        self.id = id
        self.islem_no = islem_no
        self.lis_kabul_id = lis_kabul_id
        self.numune_tarihi = numune_tarihi
        self.tahlil_kodu = tahlil_kodu
        self.tahlil_deger = tahlil_deger

    @property
    def serialize(self):
        """ LabSonuc nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'islem_no': self.islem_no,
            'lis_kabul_id': self.lis_kabul_id,
            'numune_tarihi': self.numune_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'tahlil_kodu': self.tahlil_kodu,
            'tahlil_deger': self.tahlil_deger
        }
