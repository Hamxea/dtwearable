import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from kvc.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor
from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class TemperaturePredictionAIModel(AbstractUnivariateTimeSeriesSvr):
    """ Ateş değerleri üzerinden tahmin üreten sınıf. AbstractUnivariateTimeSeriesSvr sınıfından üretilir """

    hemsire_gozlem_dao = HemsireGozlemDAO()

    def __init__(self):
        self.window_size = 5

    def get_dataset(self, dataset_parameters):
        """ dataset parametrelerine göre uygun dataseti getiren metod """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']

        hemsire_gozlem_dto_list = self.hemsire_gozlem_dao.get_temperature_in_date_range(dataset_start_time, dataset_end_time)
        hemsire_gozlem_dto_list.sort(key=lambda x: x.olcum_tarihi)

        return UnivariateTimeSeriesPreprocessor().preprocess(hemsire_gozlem_dto_list, 12)