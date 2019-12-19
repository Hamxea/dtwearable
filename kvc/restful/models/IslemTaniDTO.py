from db import db

class IslemTaniDTO(db.Model):
    """ Işlem Tani tablosu için veritabanı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = "islem_tani"

    id = db.Column(db.BigInteger, primary_key=True)
    islem_no = db.Column(db.BigInteger)
    tani_kodu = db.Column(db.String)
    tani_tipi = db.Column(db.Integer)

    def __init__(self, id: int, islem_no: int, tani_kodu: str, tani_tipi: int):
        self.id = id
        self.islem_no = islem_no
        self.tani_kodu = tani_kodu
        self.tani_tipi = tani_tipi

    @property
    def serialize(self):
        """ Işlem Tani nesnesini json'a çeviren metod """

        return {
            'id': self.id,
            'islem_no': self.islem_no,
            'tani_kodu': self.tani_kodu,
            'tani_tipi': self.tani_tipi
        }
