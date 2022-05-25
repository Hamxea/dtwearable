from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.PredictionDTO import PredictionDTO


class StatisticsDAO(AbstractDAO):
    """ Class that returns success results for predicted results via database """

    def __init__(self):
        super().__init__(PredictionDTO)

    """ 
     It compares the predict values on the database with the actual values and returns a ratio.
     calls database functions
    """
    def get_success_rate_for_TemperatureModel(self):
        return None


