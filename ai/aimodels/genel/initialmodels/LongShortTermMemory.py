from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from  keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np


class LongShortTermMemory(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """


    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        global lstm_model
        global graph

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'],)
        lstm_model = self.train_lstm(X_train, y_train, dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            score, acc = self.test_lstm(lstm_model, X_test, y_test, dataset_parameters['window_size'])

        return lstm_model, {"score": score, "accuracy": acc}

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

    def train_lstm(self, X_train, y_train, window_size):
        """ Method that creates lstm model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        #window_size = 3

        # define model
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(window_size, n_features)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(n_features))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

        # fit model
        model.fit(X_train, y_train, epochs=400, verbose=0)

        return model

    def test_lstm(self, lstm_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created lstm model """
        #window_size = 3
        # flatten input and choose the features

        X_test = X_test[np.size(X_test, 0)-1:, :]
        print(X_test)
        print(type(X_test))
        print(X_test.shape)
        n_features = X_test.shape[2]
        print(n_features)
        X_test = X_test.reshape(1, window_size, n_features)
        print(X_test)
        yha_predict = lstm_model.predict(X_test, verbose=0)
        print(yha_predict)
        print(type(X_test))
        """
        for i in range(0, np.size(X_test, 0) - 1):
           # n_features = X_test[i].shape[1]
            X_test = X_test [:,i]
            n_features = X_test.shape[1]
            print(n_features)
            print(X_test)
            X_test = X_test.reshape(1, window_size, n_features)
            print(X_test)
            print(X_test.shape)
            #yha_predict = lstm_model.predict(X_test[i], verbose=0)
            #print(yha_predict)
            """

        """ 
        print(np.size(X_test, 0) - 1)
        for i in range(np.size(X_test, 0) - 1):
            # flatten input and choose the features
            print("next line \n")
            X_test = X_test[i]
            print(X_test[i])
            print(X_test[i].shape)
            # n_features = X_test.shape[1]
            X_test[i] = X_test[i].reshape(1, window_size, 6)
            yha_predict = lstm_model.predict(X_test[i], verbose=0)"""



        """ Evaluation function of an input given a score """
        (score, acc) = lstm_model.evaluate(X_test, yha_predict, verbose=0)
        #print("Score:", score)

        #return 1, 1
        return (score, acc)

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
