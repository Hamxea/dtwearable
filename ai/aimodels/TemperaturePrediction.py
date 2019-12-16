import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class TemperaturePrediction(AbstractUnivariateTimeSeriesSvr):
    """ Ateş değerleri üzerinden tahmin üreten sınıf. AbstractUnivariateTimeSeriesSvr sınıfından üretilir """

    hemsire_gozlem_dao = HemsireGozlemDAO()

    def __init__(self):
        self.window_size = 5

    def get_dataset(self, dataset_parameters):
        """ dataset parametrelerine göre uygun dataseti getiren metod """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']

        hemsire_gozlem_list = self.hemsire_gozlem_dao.get_fever_in_date_range(dataset_start_time, dataset_end_time)
        vucut_sicakligi_list = []
        for hemsire_gozlem in hemsire_gozlem_list:
            vucut_sicakligi_list.append(hemsire_gozlem.vucut_sicakligi)

        return pd.DataFrame({'col': vucut_sicakligi_list})