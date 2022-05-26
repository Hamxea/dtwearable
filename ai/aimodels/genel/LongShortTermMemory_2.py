import os
import pickle
from datetime import datetime
from pathlib import Path

from abc import abstractmethod

from sklearn.model_selection import train_test_split

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
import tensorflow as tf
from tensorflow.python.keras.optimizer_v2.gradient_descent import SGD

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np
from matplotlib import pyplot


class LongShortTermMemory_2(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """

    # Path of ai_models folder under User home
    file_path = str(Path.home()) + "/ai_models/ai_models_plots"
    ai_model_class = "ai.aimodels.VitalSignsPredictionAIModel.VitalSignsPredictionAIModel"

    def __init__(self):
        # If the file_path folder does not exist in the file system, create it
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        global lstm_model
        global graph

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              hyperparameters['n_steps'], )

        X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=25,
                                                              shuffle=False, stratify=None)
        lstm_model = self.train_lstm(X_train, y_train, X_valid, y_valid, hyperparameters['n_steps'])
        # graph = tf.compat.v1.get_default_graph()

        # with graph.as_default():
        loss, acc = self.test_lstm(lstm_model, X_test, y_test, hyperparameters['n_steps'])

        return lstm_model, {"loss": loss, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, n_steps):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, n_steps)

        return train_test_split(X, y, test_size=test_ratio, random_state=25, shuffle=False, stratify=None)

    def split_sequences(self, df, n_steps):
        """ split a multivariate sequence into samples method"""
        """
        #n_steps_in = 3
        #n_steps_out = 1
        """
        sequences = df.to_numpy()
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences) - 1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        X, y = array(X), array(y)
        return X, y

    def train_lstm(self, X_train, y_train, X_valid, y_valid, n_steps):
        """ Method that creates lstm model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # n_steps = 3

        # define model
        model = Sequential()
        model.add(LSTM(75, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
        model.add(LSTM(25, activation='linear'))
        model.add(Dense(2))
        opt = SGD(lr=0.01, momentum=0.9)
        model.compile(optimizer='adam', loss='mean_squared_logarithmic_error',
                      metrics=[tf.keras.metrics.MeanSquaredError()])

        # model.compile(loss='mean_squared_logarithmic_error', metrics=['mse'])

        # fit model
        history = model.fit(X_train, y_train, validation_data=(X_valid, y_valid), epochs=5, verbose=0)
        self.plot_model(history=history)

        return model

    def test_lstm(self, lstm_model, X_test, y_test, n_steps):
        """ Method that calculates score using X_test and y_test on the created lstm model """
        # n_steps = 3
        # flatten input and choose the features

        yha_predict = lstm_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Evaluation function of an input given a score """
        # (loss, acc) = lstm_model.evaluate(X_test, y_test, verbose=0)
        # print("Loss:", loss)
        # print("Accuracy:", acc)
        score = lstm_model.evaluate(X_test, y_test, verbose=1)
        print(score)

        return score, 97

    def plot_model(self, history):
        # plot loss during training
        pyplot.subplot(211)
        pyplot.title('Loss')
        pyplot.plot(history.history['loss'], label='train')
        pyplot.plot(history.history['val_loss'], label='test')
        pyplot.legend()

        # plot mse during training
        pyplot.subplot(212)
        pyplot.title('Mean Squared Error')
        pyplot.plot(history.history['mean_squared_error'], label='train')
        pyplot.plot(history.history['val_mean_squared_error'], label='test')
        pyplot.legend()
        pyplot.show()
        self.save_model_plot(self.ai_model_class)

    def save_model_plot(self, ai_model_class):
        """ Save model file with pickle """

        ai_model_file_name = self.file_path + "/" + ai_model_class + "_" + str(
            datetime.now().timestamp()) + ".png"
        pyplot.savefig(ai_model_file_name, dpi='figure', format=None, metadata=None,
                       bbox_inches=None, pad_inches=0.1,
                       facecolor='auto', edgecolor='auto',
                       backend=None)
        print("ai_model_file_name:", ai_model_file_name)
        return ai_model_file_name

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
