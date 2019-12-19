import datetime

from db import db


class IslemDTO(db.Model):
    """
    Islem tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı
    """

    __tablename__ = "islem"

    islem_no = db.Column(db.Integer, primary_key=True)
    kayit_tarihi = db.Column(db.DateTime)
    # cinsiyet = db.Column(IntEnum(CinsiyetEnum))
    cinsiyet = db.Column(db.Integer)
    yas = db.Column(db.SmallInteger)
    operasyon_tarihi = db.Column(db.DateTime)
    cikis_tarihi = db.Column(db.DateTime)
    # etiket = db.Column(IntEnum(KVCLabelEnum))
    etiket = db.Column(db.Integer)

    # islem_operasyon_list = db.relationship('IslemOperasyon', backref="islem_operasyon", lazy='dynamic')
    # hemsire_gozlem_list = db.relationship('HemsireGozlem', backref="hemsire_gozlem", lazy='dynamic')

    def __init__(self, islem_no: int, kayit_tarihi: datetime, cinsiyet: int,
                 yas: int, operasyon_tarihi: datetime, cikis_tarihi: datetime, etiket: int):
        self.islem_no = islem_no
        self.kayit_tarihi = kayit_tarihi
        self.cinsiyet = cinsiyet
        self.yas = yas
        self.operasyon_tarihi = operasyon_tarihi
        self.cikis_tarihi = cikis_tarihi
        self.etiket = etiket

    @property
    def serialize(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'islem_no': self.islem_no,
            'kayit_tarihi': self.kayit_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'cinsiyet': self.cinsiyet,
            'yas': self.yas,
            'operasyon_tarihi': self.operasyon_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'cikis_tarihi': self.cikis_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'etiket': self.etiket
            # 'islem_operrasyon_list': [islem_operasyon.json() for islem_operasyon in self.islem_operasyon_list.all()]
        }
