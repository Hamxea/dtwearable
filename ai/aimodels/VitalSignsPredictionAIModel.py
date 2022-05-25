import datetime
from itertools import chain

from keras import backend as K

import pandas as pd

from ai.aimodels.genel.LongShortTermMemory_2 import LongShortTermMemory_2

from dt.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class VitalSignsPredictionAIModel(LongShortTermMemory_2):
    """ Genel Tahmin üretin TEST sınıfı..hangi ozellik belli olmadı için, hemşire gozlem veri testlendir.
     TODO....PatientStatusPredictionAIModel sınıfından üretilir """

    hemsire_gozlem_dao = HemsireGozlemDAO()
    window_size = 3

    def get_dataset(self, dataset_parameters):
        """ dataset parametrelerine göre uygun dataseti getiren metod """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']
        dataset_window_size = dataset_parameters['window_size']
        dataset_column_names_list = []
        for i in range(dataset_window_size):
            dataset_column_names_list.append('F' + str(i))

        data = pd.read_csv('data/cardio_train.csv', sep=';')
        df_data = data[["ap_hi", "ap_lo"]]

        return df_data

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Modelin belirli tarih aralığındaki istatistiklerini getirmek için kullanılan metot
            Bu model için şu aşamada istatistik üretilmediği için boş json dönüyor
        """

        return {}

    def predict(self, islem_no):
        pass
        return
