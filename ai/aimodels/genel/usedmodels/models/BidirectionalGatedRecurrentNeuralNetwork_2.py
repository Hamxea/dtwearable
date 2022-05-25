import errno
import os
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from keras.regularizers import l2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Bidirectional, GRU, Dropout
import matplotlib.pyplot as plt

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array


class BidirectionalGatedRecurrentNeuralNetwork_2(AbstractAIModel):
    """ Bidirectional Gated Recurrent Neural Network (bil_gru) with 1-Step Output """

    global bil_gru_model
    global graph
    global EPOCHS
    EPOCHS = 25

    # User home altında ai_models klasörünün path'i
    file_path_plot = os.path.join("ai_models", "ai_models_plots")

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        bil_gru_model = self.train_bil_gru(X_train, y_train, X_test, y_test, dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            acc, loss = self.test_bil_gru(bil_gru_model, X_test, y_test, dataset_parameters['window_size'])

        return bil_gru_model, {"accuracy": acc, "loss": loss}

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
            X.append(seq_x[:, :-1])
            y.append(seq_y[-1:])
        X, y = array(X), array(y)
        return X, y

    def train_bil_gru(self, X_train, y_train, X_test, y_test, window_size):
        """ Method that creates a bil_gru model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # window_size = 3

        # define model
        model = Sequential()
        model.add(Bidirectional(GRU(100, activation='relu', return_sequences=True, input_shape=(window_size, n_features),
                                    kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01),
                                    bias_regularizer=l2(0.01))))
        model.add(Bidirectional(GRU(100, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu')))
        model.add(Dropout(0.5))
        model.add(Dense(6, kernel_regularizer=l2(0.01), activation='softmax'))
        # print(model.summary())
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])

        # fit model
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=EPOCHS, verbose=0)
        self.plot_model(history, EPOCHS, class_name=__name__)

        return model

    def test_bil_gru(self, bil_gru_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created bil_gru model """

        yha_predict = bil_gru_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Evaluation function of an input given a score """
        (loss, acc) = bil_gru_model.evaluate(X_test, y_test, verbose=0)
        print("Loss:", loss)
        print("Accuracy:", acc)

        return acc, loss

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
