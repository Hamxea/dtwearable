from keymind.daos.AbstractDAO import AbstractDAO
from keymind.models.Prediction import Prediction

class PredictionDAO(AbstractDAO):
    """ Prediction nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def find_by_id(self, _id):
        """ _id değerine göre Prediction nesnesini veritabanından getiren metod """

        return Prediction.query.filter_by(id=_id).first()

