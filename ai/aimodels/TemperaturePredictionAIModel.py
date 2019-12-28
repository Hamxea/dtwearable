from datetime import datetime

import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from kvc.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor
from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class TemperaturePredictionAIModel(AbstractUnivariateTimeSeriesSvr):
    """ Ateş değerleri üzerinden tahmin üreten sınıf. AbstractUnivariateTimeSeriesSvr sınıfından üretilir """

    time_interval_in_hours = 12
    window_size = 3

    hemsire_gozlem_dao = HemsireGozlemDAO()

    def get_dataset(self, dataset_parameters):
        """ dataset parametrelerine göre uygun dataseti getiren metod """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']
        dataset_window_size = dataset_parameters['window_size']
        dataset_column_names_list = []
        for i in range(dataset_window_size):
            dataset_column_names_list.append('F' + str(i))


        hemsire_gozlem_dto_list = self.hemsire_gozlem_dao.get_temperature_in_date_range(dataset_start_time, dataset_end_time)
        hemsire_gozlem_dto_list.sort(key=lambda x: x.olcum_tarihi)

        return UnivariateTimeSeriesPreprocessor().preprocess(sorted_dto_list=hemsire_gozlem_dto_list,
                                                             feature_name='vucut_sicakligi', time_interval_in_hours=self.time_interval_in_hours,
                                                             window_size=dataset_window_size, column_list=dataset_column_names_list)

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Modelin belirli tarih aralığındaki istatistiklerini getirmek için kullanılan metot
            Bu model için şu aşamada istatistik üretilmediği için boş json dönüyor
        """

        return {}

    def predict(self, islem_no):

        # TODO sil
        feature_values_for_prediction = self.hemsire_gozlem_dao.get_feature_values_for_prediction()


        pass
    """
     veriyi al
     tahmine yolla
     sonuç dön
    """
