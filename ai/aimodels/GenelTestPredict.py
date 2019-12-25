import pandas as pd

from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from ai.aimodels.genel.MultilayerPerceptronMultiStepOutput import MutlilayerPerceptronMultiStepOutput
from ai.aimodels.genel.MultilayerPerceptron import MutlilayerPerceptron
from ai.aimodels.genel.VectorAutoRegression import VectorAutoRegression

from kvc.restful.daos.HemsireGozlemDAO import HemsireGozlemDAO


class GenelTestPredict(AbstractUnivariateTimeSeriesSvr):
    """ Ateş değerleri üzerinden tahmin üreten sınıf. AbstractUnivariateTimeSeriesSvr sınıfından üretilir """

    hemsire_gozlem_dao = HemsireGozlemDAO()

    def __init__(self):
        self.window_size = 5

    def get_dataset(self, dataset_parameters):
        """ dataset parametrelerine göre uygun dataseti getiren metod """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']

        hemsire_gozlem_list = self.hemsire_gozlem_dao.get_fever_in_date_range(dataset_start_time, dataset_end_time)
        hemsire_gozlem_final_list = []
        hemsire_gozlem_nabiz_list = []
        hemsire_gozlem_tansiyon_sis_list = []
        hemsire_gozlem_tansiyon_dias_list = []
        hemsire_gozlem_spo_list = []
        hemsire_gozlem_o2_list = []
        hemsire_gozlem_kan_transfuzyonu_list = []

        for hemsire_gozlem in hemsire_gozlem_list:
            #hemsire_gozlem_final_list.append(int(hemsire_gozlem.vucut_sicakligi))
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
        return df_hemsire_gozlem # pd.DataFrame({'col': hemsire_gozlem_final_list})
