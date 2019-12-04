from db import db

"""
Veritabanı işlkemlerinin gerçekleştirildiği DAO neslerinin Abstract sınıfı
Ortak kullanılan veritabanı işlemleri bu metod içerisinde tanımlanır
"""
class AbstractDAO:

    # Model nesnesini veritabanına kaydeden veya id varsa güncelleyen metod
    def save_to_db(self, model):
        db.session.add(model)
        db.session.commit()

    # Model nesnesini veritabanından silen metod
    def delete_from_db(self, model):
        db.session.delete(model)
        db.session.commit()