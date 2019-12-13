from db import db


class AbstractDAO:
    """
    Veritabanı işlkemlerinin gerçekleştirildiği DAO neslerinin Abstract sınıfı
    Ortak kullanılan veritabanı işlemleri bu metod içerisinde tanımlanır
    """

    model = None

    def __init__(self, model):
        self.model = model

    def save_to_db(self, model):
        """ Model nesnesini veritabanına kaydeden veya id varsa güncelleyen metod """

        db.session.add(model)
        db.session.commit()

    def find_by_id(self, _id: int):
        """ _id değerine göre LabSonuc nesnesini veritabanından getiren metod """

        return self.model.query.filter_by(id=_id).first()

    def delete_from_db(self, model):
        """ Model nesnesini veritabanından silen metod """

        db.session.delete(model)
        db.session.commit()
