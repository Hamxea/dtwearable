from datetime import datetime

from db import db


class LabSonucDTO(db.Model):
    """ Laboratuvar Sonuçları tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "lab_sonuc"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_id = db.Column(db.BigInteger)
    numune_tarihi = db.Column(db.DateTime)
    tahlil_id = db.Column(db.BigInteger)
    tahlil_adi = db.Column(db.String)
    tahlil_deger = db.Column(db.String)

    def __init__(self, id: int, islem_id: int, numune_tarihi: datetime, tahlil_id: int, tahlil_adi: str, tahlil_deger:str):
        self.id = id
        self.islem_id = islem_id
        self.numune_tarihi = numune_tarihi
        self.tahlil_id = tahlil_id
        self.tahlil_adi = tahlil_adi
        self.tahlil_deger = tahlil_deger

    @property
    def serialize(self):
        """ LabSonuc nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'numune_tarihi': self.numune_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'tahlil_id': self.tahlil_id,
            'tahlil_adi': self.tahlil_adi,
            'tahlil_deger': self.tahlil_deger
        }
