import datetime
from builtins import float

from db import db


class SiviAlimi(db.Model):
    """ Sıvı Alımı tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "sivi_alimi"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_id = db.Column(db.BigInteger)
    olcum_tarihi = db.Column(db.DateTime)
    kilo = db.Column(db.Float)
    aldigi_sivi_miktari_oral = db.Column(db.Float)
    aldigi_sivi_miktari_intravanoz = db.Column(db.Float)
    aldigi_sivi_miktari_nazogastrik = db.Column(db.Float)
    cikardigi_sivi_miktari_idrar = db.Column(db.Float)
    cikardigi_sivi_miktari_nazogastrik = db.Column(db.Float)
    cikardigi_sivi_diren = db.Column(db.Float)
    sivi_farki = db.Column(db.Float)

    # sivi_alimi_list = db.relationship('SiviAlimi', backref="sivi_alimi", lazy='dynamic')

    def __init__(self, id: int, islem_id: int, olcum_tarihi: datetime, kilo: float, aldigi_sivi_miktari_oral: float, aldigi_sivi_miktari_intravanoz: float,
                 aldigi_sivi_miktari_nazogastrik: float, cikardigi_sivi_miktari_idrar: float, cikardigi_sivi_miktari_nazogastrik: float, cikardigi_sivi_diren: float, sivi_farki: float):

        self.id = id
        self.islem_id = islem_id
        self.olcum_tarihi = olcum_tarihi
        self.kilo = kilo
        self.aldigi_sivi_miktari_oral = aldigi_sivi_miktari_oral
        self.aldigi_sivi_miktari_intravanoz = aldigi_sivi_miktari_intravanoz
        self.aldigi_sivi_miktari_nazogastrik = aldigi_sivi_miktari_nazogastrik
        self.cikardigi_sivi_miktari_idrar = cikardigi_sivi_miktari_idrar
        self.cikardigi_sivi_miktari_nazogastrik = cikardigi_sivi_miktari_nazogastrik
        self.cikardigi_sivi_diren = cikardigi_sivi_diren
        self.sivi_farki = sivi_farki

    @property
    def serialize(self):
        """ Sıvı Alımı nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'olcum_tarihi': self.olcum_tarihi.strftime('%d.%m.%Y %H:%M:%S'),
            'kilo': self.kilo,
            'aldigi_sivi_miktari_oral': self.aldigi_sivi_miktari_oral,
            'aldigi_sivi_miktari_intravanoz': self.aldigi_sivi_miktari_intravanoz,
            'aldigi_sivi_miktari_nazogastrik': self.aldigi_sivi_miktari_nazogastrik,
            'cikardigi_sivi_miktari_idrar': self.cikardigi_sivi_miktari_idrar,
            'cikardigi_sivi_miktari_nazogastrik': self.cikardigi_sivi_miktari_nazogastrik,
            'cikardigi_sivi_diren': self.cikardigi_sivi_diren,
            'sivi_farki': self.sivi_farki
            # 'islem_operrasyon_list': [islem_operasyon.json() for islem_operasyon in self.islem_operasyon_list.all()]
        }
