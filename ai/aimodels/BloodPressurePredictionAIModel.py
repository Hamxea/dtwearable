from datetime import datetime
import pandas as pd

from ai.aimodels.AbstractBloodPressureTimeSeriesSvr import AbstractBloodPressureTimeSeriesSvr
from ai.aimodels.AbstractUnivariateTimeSeriesSvr import AbstractUnivariateTimeSeriesSvr
from dt.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor
from dt.preprocessing.UnivariateVitalSignsTimeSeriesPreprocessor import UnivariateVitalSignsTimeSeriesPreprocessor


class BloodPressurePredictionAIModel(AbstractBloodPressureTimeSeriesSvr):
    """ Class that generates predictions based on fire values. Generated from AbstractUnivariateTimeSeriesSvr """

    def get_dataset(self, dataset_parameters):
        """ method that returns the appropriate dataset according to the dataset parameters """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']
        dataset_window_size = dataset_parameters['window_size']
        dataset_column_names_list = []
        for i in range(dataset_window_size):
            dataset_column_names_list.append('F' + str(i))

        # hemsire_gozlem_dto_list = self.hemsire_gozlem_dao.get_temperature_in_date_range(dataset_start_time, dataset_end_time)
        # hemsire_gozlem_dto_list.sort(key=lambda x: x.olcum_date)

        data = pd.read_csv('/Users/hamzaharunamohammed/Desktop/Ntnu/PhD/Development/dtwearable/'
                                'data/cardio_train.csv', sep=';')
        #data_list = list(data)

        return UnivariateVitalSignsTimeSeriesPreprocessor().preprocess(sorted_dto_list=data,
                                                             feature_name='ap_hi', time_interval_in_hours=12,
                                                             window_size=dataset_window_size, column_list=dataset_column_names_list)

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ The method used to fetch the statistics of the model for a certain date range
            Empty json is returned because statistics are not produced for this model at this stage.
        """

        return {}