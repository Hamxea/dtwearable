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
        try:
            db.session.add(model)
            db.session.commit()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't save into database! Object name is '{}'".format(type(model).__name__))

    def find_by_id(self, _id: int):
        """ _id değerine göre LabSonuc nesnesini veritabanından getiren metod """

        try:
            return self.model.query.filter_by(id=_id).first()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't find in database! Id is '{}'".format(id))

    def delete_from_db(self, model):
        """ Model nesnesini veritabanından silen metod """
        try:
            db.session.delete(model)
            db.session.commit()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't delete from database! Object name is '{}'".format(type(model).__name__))
