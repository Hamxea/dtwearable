import datetime
from itertools import chain

from keras import backend as K

import pandas as pd

from ai.aimodels.genel.LongShortTermMemory_2 import LongShortTermMemory_2


class VitalSignsPredictionAIModel(LongShortTermMemory_2):
    """ Generate General Prediction TEST class..w.
     TODO....PatientStatusPredictionAIModel and RuleEngines """

    window_size = 3

    def get_dataset(self, dataset_parameters):
        """ Method that returns the appropriate dataset according to the dataset parameters """

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
        """ The method used to fetch the statistics of the model for a certain date range
             Empty json is returned because statistics are not produced for this model at this stage.
        """

        return {}

    def predict(self, islem_no):
        pass
        return
