import datetime
from kvc.restful.models.enums.IntEnum import IntEnum

from db import db
from kvc.restful.models.enums.OperasyonTipiEnum import OperasyonTipiEnum


class IslemOperasyonDTO(db.Model):
    """
    Islem Operasyon tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı
    """

    __tablename__ = "islem_operasyon"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_id = db.Column(db.BigInteger)
    operasyon_sut = db.Column(db.String)
    operasyon_tipi = db.Column(IntEnum(OperasyonTipiEnum))

    def __init__(self, id: int, islem_id: int,operasyon_sut:str,operasyon_tipi:int):
        self.id = id
        self.islem_id  = islem_id
        self.operasyon_sut  = operasyon_sut
        self.operasyon_tipi = operasyon_tipi

    @property
    def serialize(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'operasyon_sut' :self.operasyon_sut,
            'operasyon_tipi' : self.operasyon_tipi.name
        }