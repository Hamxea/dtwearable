from db import db

class AbstractDAO:
    """
    Veritabanı işlkemlerinin gerçekleştirildiği DAO neslerinin Abstract sınıfı
    Ortak kullanılan veritabanı işlemleri bu metod içerisinde tanımlanır
    """

    def save_to_db(self, model):
        """ Model nesnesini veritabanına kaydeden veya id varsa güncelleyen metod """

        db.session.add(model)
        db.session.commit()


    def delete_from_db(self, model):
        """ Model nesnesini veritabanından silen metod """

        db.session.delete(model)
        db.session.commit()