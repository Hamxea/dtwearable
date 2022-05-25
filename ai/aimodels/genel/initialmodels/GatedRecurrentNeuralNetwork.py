from abc import abstractmethod
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np


class GatedRecurrentNeuralNetwork(AbstractAIModel):
    """ Gated Recurrent Neural Network (gru) with 1-Step Output """

    global gru_model
    global graph

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        gru_model = self.train_gru(X_train, y_train, dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            # score, acc
            score = self.test_gru(gru_model, X_test, y_test, dataset_parameters['window_size'])

        return gru_model, {"score": score}  # {"score": score, "accuracy": acc}

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

    def train_gru(self, X_train, y_train, window_size):
        """ Method that creates gru model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # window_size = 3

        # define model
        model = Sequential()
        model.add(GRU(100, activation='relu', return_sequences=True, input_shape=(window_size, n_features)))
        model.add(GRU(100, activation='relu'))
        model.add(Dense(n_features))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

        # fit model
        model.fit(X_train, y_train, epochs=400, verbose=0)

        return model

    def test_gru(self, gru_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created gru model """

        """ Evaluation function of an input given a score """
        score = gru_model.evaluate(X_test, y_test, verbose=0)
        score = round(score[1], 3)

        # window_size = 3
        X_test = X_test[np.size(X_test, 0) - 1:, :]
        # flatten input and choose the features
        n_features = X_test.shape[2]
        X_test = X_test.reshape(1, window_size, n_features)
        yha_predict = gru_model.predict(X_test, verbose=0)
        print(yha_predict)

        return score

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
