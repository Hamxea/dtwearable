from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.PredictionDTO import PredictionDTO


class PredictionDAO(AbstractDAO):
    """ Prediction nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(PredictionDTO)

