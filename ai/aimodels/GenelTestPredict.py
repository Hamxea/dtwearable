import datetime

import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from ai.aimodels.genel.LongShortTermMemory import LongShortTermMemory
from ai.aimodels.genel.MultilayerPerceptronMultiStepOutput import MutlilayerPerceptronMultiStepOutput
from ai.aimodels.genel.MultilayerPerceptron import MutlilayerPerceptron
from ai.aimodels.genel.VectorAutoRegression import VectorAutoRegression
from ai.aimodels.genel.ConvolutionalNeuralNetworkMultiStepOutput import ConvolutionalNeuralNetworkMultiStepOutput
from ai.aimodels.genel.ConvolutionalNeuralNetwork import ConvolutionalNeuralNetwork
from kvc.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor

from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class GenelTestPredict(LongShortTermMemory):
    """ Genel Tahmin üretin sınıfı..hangi ozellik belli olmadı için, hemşire gozlem veri testlendir.
     AbstractUnivariateTimeSeriesSvr sınıfından üretilir """

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


        hemsire_gozlem_dto_list = self.hemsire_gozlem_dao.\
            get_temperature_in_date_range(dataset_start_time, dataset_end_time)
        hemsire_gozlem_dto_list.sort(key=lambda x: x.olcum_tarihi)

        hemsire_gozlem_final_list = []
        hemsire_gozlem_nabiz_list = []
        hemsire_gozlem_tansiyon_sis_list = []
        hemsire_gozlem_tansiyon_dias_list = []
        hemsire_gozlem_spo_list = []
        hemsire_gozlem_o2_list = []
        hemsire_gozlem_kan_transfuzyonu_list = []

        for hemsire_gozlem in hemsire_gozlem_dto_list:
            # hemsire_gozlem_final_list.append(int(hemsire_gozlem.vucut_sicakligi))
            hemsire_gozlem_nabiz_list.append(hemsire_gozlem.nabiz)
            hemsire_gozlem_tansiyon_sis_list.append(hemsire_gozlem.tansiyon_sistolik)
            hemsire_gozlem_tansiyon_dias_list.append(hemsire_gozlem.tansiyon_diastolik)
            hemsire_gozlem_spo_list.append(hemsire_gozlem.spo)
            hemsire_gozlem_o2_list.append(hemsire_gozlem.o2)
            hemsire_gozlem_kan_transfuzyonu_list.append(hemsire_gozlem.kan_transfuzyonu)

        hemsire_gozlem_final_list.append(hemsire_gozlem_nabiz_list)
        hemsire_gozlem_final_list.append(hemsire_gozlem_tansiyon_sis_list)
        hemsire_gozlem_final_list.append(hemsire_gozlem_tansiyon_dias_list)
        hemsire_gozlem_final_list.append(hemsire_gozlem_spo_list)
        hemsire_gozlem_final_list.append(hemsire_gozlem_o2_list)
        hemsire_gozlem_final_list.append(hemsire_gozlem_kan_transfuzyonu_list)

        df_hemsire_gozlem = pd.DataFrame(hemsire_gozlem_final_list).transpose()
        return df_hemsire_gozlem  # pd.DataFrame({'col': hemsire_gozlem_final_list})


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


    """
        return UnivariateTimeSeriesPreprocessor().preprocess(sorted_dto_list=df_hemsire_gozlem,
                                                             feature_name='vucut_sicakligi', time_interval_in_hours=12,
                                                             window_size=dataset_window_size, column_list=dataset_column_names_list)
                                                             
                                                             
                                                            """
