from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.PredictionDTO import PredictionDTO


class PredictionDAO(AbstractDAO):
    """ Contains the methods by which database operations are performed for the Prediction object """

    def __init__(self):
        super().__init__(PredictionDTO)

