from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.statespace.varmax import VARMAX
from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoregressionMovingAverageExogenousRegressors(AbstractAIModel):
    """ Vector Autoregression Moving-Average with Exogenous Regressors (VARMAX)with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, dataset_parameters['test_ratio'], hyperparameters['n_steps'])
        mlp_model = self.train_mlp(train_data, hyperparameters['n_steps'])
        score, acc = self.test_mlp(mlp_model, test_data)

        return mlp_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, n_Steps):
        """ Method that divides dataset for train and test """

        train_data = df[:int((1-test_ratio)*len(df))]
        test_data = df[int((1-test_ratio)*len(df)):]

        return train_data, test_data

    def train_mlp(self, train_data, n_steps):
        """ Method that creates mlp model using x_train and y_train """

        model = VARMAX(train_data, order=(1, 1))
        model_fit = model.fit(disp=False)
        return model_fit

    def test_mlp(self, mlp_model, test_data):
        """ Method that calculates score using X_test and y_test on the created mlp model """

        #make prediction of test validation data
        prediction = mlp_model.forecast(exog=test_data)
        print(prediction)

        return 0, 0

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
