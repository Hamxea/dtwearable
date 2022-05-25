from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR

from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoRegression(AbstractAIModel):
    """ Vector Auto Regression (VAR) with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, dataset_parameters['test_ratio'], dataset_parameters['window_size'])
        var_model = self.train_var(train_data, dataset_parameters['window_size'])
        score, acc = self.test_var(var_model, test_data)

        return var_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        train_data = df[:int((1 - test_ratio) * len(df))]
        test_data = df[int((1 - test_ratio) * len(df)):]

        return train_data, test_data

    def train_var(self, train_data, window_size):
        """ Method that creates the var model using x_train and y_train """

        model = VAR(endog=train_data)
        model_fit = model.fit()
        return model_fit

    def test_var(self, var_model, test_data):
        """ Method that calculates score using X_test and y_test on the created var model """

        # make prediction of test validation data with 1 step_out
        # var_model.y
        prediction = var_model.forecast(test_data.to_numpy(), steps=1)
        print(prediction)

        return 1, 0

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
