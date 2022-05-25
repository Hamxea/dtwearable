from abc import abstractmethod

from numpy import array
import numpy as np
from sklearn.model_selection import train_test_split

from ai.aimodels.AbstractAIModel import AbstractAIModel
# Load the statsmodels api
import statsmodels.api as sm



class AlgorithmTest(AbstractAIModel):
    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'],)
        mlp_model = self.train_mlp(X_train, y_train)
        score, acc = self.test_mlp(mlp_model, X_test, y_test)

        return mlp_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, window_size)

        return train_test_split(X, y, test_size=test_ratio, shuffle=False, stratify=None)

    def split_sequences(self, df, window_size):
        """ split a multivariate sequence into samples method"""
        """
        #window_size_in = 3
        #window_size_out = 1
        """
        sequences = df.to_numpy()
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + window_size
            # check if we are beyond the dataset
            if end_ix > len(sequences) - 1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        X, y = array(X), array(y)
        return X, y

    def train_mlp(self, X_train, y_train):
        """ Method that creates mlp model using x_train and y_train """

        # flatten input
        n_input = X_train.shape[1] * X_train.shape[2]
        X_train = X_train.reshape((X_train.shape[0], n_input))
        # flatten output
        n_output = y_train.shape[1]

        # Fit a local level model
        model = sm.tsa.VARMAX(X_train, order=(1, 0))
        # Note that mod_var1 is an instance of the VARMAX class
        # Fit the model via maximum likelihood
        model = model.fit()
        # Note that res_var1 is an instance of the VARMAXResults class
        print(model.summary())

        return model

    def test_mlp(self, mlp_model, X_test, y_test):
        """ Method that calculates score using X_test and y_test on the created mlp model """

        pass

        return 0, 1

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
