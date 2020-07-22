import datetime
from itertools import chain

from keras import backend as K

import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from ai.aimodels.genel.AlgorithmTest import AlgorithmTest
from ai.aimodels.genel.BidirectionalGatedRecurrentNeuralNetwork import BidirectionalGatedRecurrentNeuralNetwork
from ai.aimodels.genel.BidirectionalLongShortTermMemory import BidirectionalLongShortTermMemory
from ai.aimodels.genel.GatedRecurrentNeuralNetwork import GatedRecurrentNeuralNetwork
from ai.aimodels.genel.LongShortTermMemory import LongShortTermMemory
from ai.aimodels.genel.RecurrentNeuralNetwork import RecurrentNeuralNetwork
from ai.aimodels.genel.MultilayerPerceptronMultiStepOutput import MutlilayerPerceptronMultiStepOutput
from ai.aimodels.genel.MultilayerPerceptron import MutlilayerPerceptron
from ai.aimodels.genel.TimeDistributedNeuralNetwork import TimeDistributedNeuralNetwork
from ai.aimodels.genel.VectorAutoRegression import VectorAutoRegression
from ai.aimodels.genel.VectorAutoRegressionMovingAverage import VectorAutoregressionMovingAverage
from ai.aimodels.genel.ConvolutionalNeuralNetworkMultiStepOutput import ConvolutionalNeuralNetworkMultiStepOutput
from ai.aimodels.genel.ConvolutionalNeuralNetwork import ConvolutionalNeuralNetwork
from ai.aimodels.genel.VectorAutoregressionMovingAverageExogenousRegressors import \
    VectorAutoregressionMovingAverageExogenousRegressors
from kvc.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor

from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class GenelTestPredict(GatedRecurrentNeuralNetwork):
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

        hemsire_gozlem_dto_list = self.hemsire_gozlem_dao.\
            get_temperature_in_date_range(dataset_start_time, dataset_end_time)
        hemsire_gozlem_dto_list.sort(key=lambda x: x.olcum_tarihi)

        # hemşire gozlem list dto yukarıda zaman arası
        """
        hmg_nabiz_list, hmg_tansiyon_sis_list, hmg_tansiyon_dias_list, \
        hmg_spo_list, hmg_o2_list, hmg_kan_transfuzyonu_list = ([],) * 6
        """

        hmg_nabiz_list = []
        hmg_tansiyon_sis_list = []
        hmg_tansiyon_dias_list = []
        hmg_spo_list = []
        hmg_o2_list = []
        hmg_kan_transfuzyonu_list = []

        for hemsire_gozlem in hemsire_gozlem_dto_list:
            # hemsire_gozlem_final_list.append(int(hemsire_gozlem.vucut_sicakligi))
            hmg_nabiz_list.append(hemsire_gozlem.nabiz)
            hmg_tansiyon_sis_list.append(hemsire_gozlem.tansiyon_sistolik)
            hmg_tansiyon_dias_list.append(hemsire_gozlem.tansiyon_diastolik)
            hmg_spo_list.append(hemsire_gozlem.spo)
            hmg_o2_list.append(hemsire_gozlem.o2)
            hmg_kan_transfuzyonu_list.append(hemsire_gozlem.kan_transfuzyonu)

        hemsire_gozlem_final_list = list(chain([hmg_nabiz_list, hmg_tansiyon_sis_list, hmg_tansiyon_dias_list,
                                                hmg_spo_list, hmg_o2_list, hmg_kan_transfuzyonu_list]))

        df_hemsire_gozlem = pd.DataFrame(hemsire_gozlem_final_list).transpose()

        K.clear_session()
        return df_hemsire_gozlem  # pd.DataFrame({'col': hemsire_gozlem_final_list})

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Modelin belirli tarih aralığındaki istatistiklerini getirmek için kullanılan metot
            Bu model için şu aşamada istatistik üretilmediği için boş json dönüyor
        """

        return {}

    def predict(self, islem_no):
        pass
        return
